from microconventions import Memo, Activity, Genre

def test_memo():
    memo = Memo(activity=Activity.set,genre=Genre.repository, success=5, execution=1, data={'my_no':13})
    d = memo.to_dict(flatten_data=True)
    assert 'my_no' in d
    assert 'data' not in d
    d = memo.to_dict(flatten_data=False)
    assert 'data' in d
    memo1 = memo.replace(genre=Genre.balance)
    d1 = memo1.to_dict()
    assert 'my_no' in d1
    assert memo1.genre == Genre.balance

