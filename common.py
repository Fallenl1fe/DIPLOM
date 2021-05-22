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
    if p == None:
        return False
    else:
        return True


#def