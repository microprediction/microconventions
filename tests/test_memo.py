from microconventions import Memo, Activity, Genre
import sys


def test_memo():
    if sys.version_info.major>=3 and sys.version_info.minor>=7:
        memo = Memo(activity=Activity.set,genre=Genre.repository, success=5, execution=1, data={'my_no':13})
    else:
        # <3.7 we need to supply all arguments
        memo = Memo(activity=Activity.set, genre=Genre.repository, success=5, execution=1, data={'my_no':13},
                    warned=0, recipient='nobody',sender='nobody',write_key='asdf',message='blah')
    d = memo.to_dict(flatten_data=True)
    assert 'my_no' in d
    assert 'data' not in d
    d = memo.to_dict(flatten_data=False)
    assert 'data' in d
    memo1 = memo.replace(genre=Genre.balance)
    d1 = memo1.to_dict()
    assert 'my_no' in d1
    assert memo1.genre == Genre.balance

