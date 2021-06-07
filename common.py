import datetime
import random

from sqlalchemy import and_

import models


def get_tests_for_user(user_id, session):
    tests_user = session.query(models.Tests).join(models.User_test
                                                  # , models.Tests.id == models.User_test.test_id
                                                  ).filter(user_id == models.User_test.user_id).all()
    return tests_user


def dostup_k_test(user_id, test_id, session):
    p = session.query(models.User_test).\
        filter(models.User_test.user_id == user_id).\
        filter(models.User_test.test_id == test_id).first()
    #p2 = session.query(models.Testing).filter(models.Testing.end_date != None)
    if p is None:
        return False
    else:
        return True


#в функции пример правила джоин
def find_actually_testing(user_id, test_id, session):
    nt = session.query(models.Testing). \
        join(models.User_test, models.User_test.test_id == models.Testing.test_id). \
        filter(models.Testing.end_date == None). \
        filter(models.User_test.user_id == user_id). \
        filter(models.User_test.test_id == test_id). \
        filter(models.User_test.date_create <= models.Testing.start_date).first()
    return nt


def get_or_create_testing(user_id, test_id, session):
    fat = find_actually_testing(user_id, test_id, session)
    if fat is None:
        return create_testing(user_id, test_id, session)
    else:
        return fat


def create_testing(user_id, test_id, session):
    testing = models.Testing(user_id=user_id, test_id=test_id)
    session.add(testing)
    session.commit()
    return testing


def get_question(user_id, test_id, session):
    q = find_actually_testing(user_id, test_id, session)
    if q == None:
        return None
    mq = session.query(models.Tests).filter(models.Tests.id==test_id).first()
    if q.current_question_id is not None:
        return q.current_question
    if q.a_number == mq.max_q:
        return None
    mass_quest_test = session.query(models.Questions). \
        filter(models.Questions.test_id == test_id).all()
    mass_quest_protocol = session.query(models.Questions). \
        join(models.Answers, models.Answers.question_id == models.Questions.id). \
        join(models.Protocols, models.Protocols.answer_id == models.Answers.id). \
        filter(models.Protocols.testing_id == q.id).all()
    mass_free_quest = []
    for i in mass_quest_test:
        est_sovpad = False
        for p in mass_quest_protocol:
            if i.id == p.id:
                est_sovpad = True
        if est_sovpad is False:
            mass_free_quest.append(i)
    ran_quest = random.choice(mass_free_quest)
    q.current_question_id = ran_quest.id
    session.commit()
    return ran_quest


def check_answer(testing_id, answer_id, session):
    protocol = models.Protocols(answer_id=answer_id, testing_id=testing_id)
    session.add(protocol)
    ans_user: models.Answers = session.query(models.Answers). \
        filter(models.Answers.id == answer_id).first()
    check_ans = ans_user.correct_a
    session.query(models.Testing).filter(models.Testing.id == testing_id).update(
        {'current_question_id': None, 'a_number': models.Testing.a_number + 1})
    if check_ans == True:
        session.query(models.Testing).filter(models.Testing.id == testing_id).update({'rating': models.Testing.rating + 1})
    q = session.query(models.Testing).filter(models.Testing.id == testing_id).first()
    mq = session.query(models.Tests).filter(models.Tests.id == q.test_id).first()
    if q.a_number == mq.max_q:
        if sdal_nesdal(testing_id=testing_id, session=session) == True:
            session.query(models.Testing).filter(models.Testing.id == testing_id).update(
                {'result': True, 'end_date': datetime.datetime.utcnow()})
            #
            session.query(models.User_test).filter(models.User_test.test_id == q.test_id).delete()
            #
        else: session.query(models.Testing).filter(models.Testing.id == testing_id).update(
                {'result': False, 'end_date': datetime.datetime.utcnow()})
    session.commit()

def sdal_nesdal(testing_id, session):
    rat = session.query(models.Testing).filter(models.Testing.id == testing_id).first()
    max_v = session.query(models.Tests).join(models.Testing, models.Tests.id == models.Testing.test_id).filter(models.Testing.id == testing_id).first()
    if rat.rating >= (max_v.max_q) * 0.7:
        return True
    else:
        return False

