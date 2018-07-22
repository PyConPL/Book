# Is your test suite wasting your time?

## Abstract
Nowadays there is no need for convincing anyone about the enormous advantages of writing automated tests for their code. Many developers had an occasion to feel total confidence in introducing changes to their codebases under the protection of vast test suites. The practice of writing tests has been widely adopted in the industry <sup>[4]</sup>, including Python world. 

Pythonistas have at their disposal the best programming language, empowering tools and tons of articles about writing tests. What can go wrong?

## Price of automated testing
Apparently, there is no such thing as a free lunch. It turns out that apart from the effort needed to write tests and update them to keep up with changes in the codebase, there is yet another cost - the time of execution. This article is to explain how essential it is to strive for the shortest execution time possible and how to achieve that.

Without tests one is stuck with manual testing. Paraphrasing article <sup>[1]</sup>, cost of manual verification can be expressed using formula:

`testing_time_without_tests = n * (setup_time + testing_time)`

...where `n` is a number of repetitions. Imagine going through such a cycle during development. If a feature that a developer is working on is relatively complex, then the expected number of repetitions will be high. Manual tests are slow by their nature. Therefore it takes a long time to get feedback whether the latest change broke something or moved a developer forward.

The situation is completely different when one has a comprehensive test suite at their disposal:

`testing_time_with_tests = n * tests_execution_time`

`n` surely will not be smaller than in the previous case. More important factor is `tests_execution_time`. If one could minimise it to a value close to zero then `n` would become irrelevant in this formula! That is exactly what we want, considering practices like Test Driven Development<sup>[5]</sup> which make a developer run tests every few seconds. It has been proved <sup>[6]</sup> that writing tests after the code is a defect-injection process. Writing code under the protection of an evolving test suite leads to far fewer mistakes and errors. Pythonista can leverage the TDD cycle provided they use it strictly for unit tests. However, the situation gets complicated when one is to deal with web applications.

There is a concept known as Test Pyramid<sup>[2]</sup>. In its original form, it assumes that unit tests should be a majority of a test suite, sometimes even 90%. Other kinds of tests, like integration and acceptance, should be a minority of the test suite. The proportion comes from the fact that unit tests are fastest to write and execute. Writing a good integration or acceptance test requires far more effort.

## What prevents Pythonistas from relying on unit tests?
A theory is one thing, real-life experience often looks differently. Without a clear testing strategy, projects usually end up with something resembling Ice-Cream Cone<sup>[3]</sup> where the majority of testing is done manually, there are some end-to-end tests and literally a few unit tests.

For example, when we write a web application using Django it might be tempting to test everything using `django.test.Client` via views. Isn't that... convenient?

```python
@pytest.mark.usefixtures('transactional_db')
def test_should_win_auction_when_no_one_else_is_bidding(
        authenticated_client: Client, auction_without_bids: Auction
) -> None:
    url = reverse('make_a_bid', args=[auction_without_bids.pk])
    expected_current_price = auction_without_bids.current_price * 10
    data = json.dumps({
        'amount': str(expected_current_price)
    })
    response = authenticated_client.post(url, data, content_type='application/json')

    assert_wins_with_current_price(response, expected_current_price)


@pytest.mark.usefixtures('transactional_db')
def test_should_not_be_winning_if_bid_lower_than_current_price(
        authenticated_client: Client, auction_without_bids: Auction
) -> None:
    url = reverse('make_a_bid', args=[auction_without_bids.pk])
    bid_price = auction_without_bids.current_price - Decimal('1.00')
    data = json.dumps({
        'amount': str(bid_price)
    })
    response = authenticated_client.post(url, data, content_type='application/json')

    assert_loses_with_current_price(response, auction_without_bids.current_price)

```

It is, indeed. Additionally, it is horribly slow.

## Where we lose most time?
There are two tests that check two basic scenarios:
1. A user makes a bid on an auction without prior bids and becomes a winner
2. A user makes a bid lower than previous winning one and therefore loses an auction

Given that our view looks as follows:
```python
@csrf_exempt
@login_required
def make_a_bid(request: HttpRequest, auction_id: int) -> HttpResponse:
    data = json.loads(request.body)
    input_dto = placing_bid.PlacingBidInputDto(
        user_id=request.user.id,
        auction_id=auction_id,
        amount=Decimal(data['amount'])
    )
    presenter = PlacingBidPresenter()
    uc = placing_bid.PlacingBidUseCase(presenter)
    uc.execute(input_dto)

    data = presenter.get_presented_data()
    if data['is_winner']:
        return HttpResponse(f'Congratulations! You are a winner! :) Current price is {data["current_price"]}')
    else:
        return HttpResponse(f'Unfortunately, you are not winning. :( Current price is {data["current_price"]}')
```

Let's carefully profile<sup>[7]</sup> one of these two tests and see where the time is spent:

`pytest  --profile tests/auctions/views/test_make_a_bid.py::test_should_not_be_winning_if_bid_lower_than_current_price`

| ncalls | tottime | percall | cumtime  | percall  | filename:lineno(function)          |
|--------|---------|---------|----------|----------|------------------------------------|
| 1      | 3e-06   | 3e-06   | 0.01078  | 0.01078  | runner.py:106(pytest_runtest_call) |
| 1      | 1.2e-05 | 1.2e-05 | 0.003892 | 0.003892 | base.py:27(reverse)                |
| 1      | 4e-06   | 4e-06   | 0.006712 | 0.006712 | client.py:522(post)                |
| 1      | 1.4e-05 | 1.4e-05 | 0.002885 | 0.002885 | placing_bid.py:43(execute)         |      |

We see that this particular test took in total 0.01078 s. Our business logic took 0.002885 s, which amounts to ~ 26 % of execution time, time of saving objects to database included. Framework code execution took 0.003892 s (url reversal) + 0.006712 s (test client) - 0.002885 s (our logic) = 0.007719 s, which is ~ 72% of the time!

The conclusion is obvious. **Overwhelming majority of the time is spent on testing the framework, not our code!**

Of course, this code is relatively simple and pytest-profiling<sup>[7]</sup> does not take into account time spent on executing fixtures (which would be sloooowly inserting objects to a database). In a real-life case, numbers would be even higher.

Let's break this down. Firstly, fixtures are run to insert the required models into the database. Tick, tock. Then Django's test client spins up and calls framework's machinery to serve the request. Tick, tock. Finally, control reaches our view that calls our logic. It starts with loading desired models from the database. Tick, tock. Then, the logic we wanted to actually test is run. We end by saving altered models back to the database. Tick, tock. Everything is green, the test passed! 

How would numbers look like if we used unit tests instead?

```python
def test_should_not_be_winning_if_bid_lower_than_current_price() -> None:
    auction = create_auction(bids=[
        Bid(id=1, bidder_id=1, amount=Decimal('10.00'))
    ])

    lower_bid = Bid(id=None, bidder_id=2, amount=Decimal('5.00'))
    auction.make_a_bid(lower_bid)

    assert lower_bid.bidder_id not in auction.winners
```

`pytest --profile tests/auctions/domain/entities/test_auction.py::test_should_not_be_winning_if_bid_lower_than_current_price`

| ncalls | tottime | percall | cumtime  | percall  | filename:lineno(function)                                                      |
|--------|---------|---------|----------|----------|--------------------------------------------------------------------------------|
| 1      | 5e-06   | 5e-06   | 0.000236 | 0.000236 | runner.py:106(pytest_runtest_call)                                             |
| 1      | 1.3e-05 | 1.3e-05 | 3.6e-05  | 3.6e-05  | test_auction.py:85(test_should_not_be_winning_if_bid_lower_than_current_price) |
| 1      | 9e-06   | 9e-06   | 1.1e-05  | 1.1e-05  | auction.py:15(make_a_bid)                                                      |

The whole test run that checks the same logic took 0.000236 s (over 12 times faster!) and method we tested took only 5% of total execution time. The rest was consumed by pytest.

That's a substantial time-saving. The situation escalates quickly when we are to check more scenarios with different edge cases. The total duration of running pytest command for 100 unit tests took 0.53 seconds while running 100 view tests with `django.test.Client` would cost a developer 25.79 seconds of their lives! Such a long time is enough for everyone to lose focus and start wondering what new posts have appeared on their Facebook boards. For the TDD cycle to work, feedback from test must not come after the time longer than 1 second!

## How to leverage unit tests?
Official Django docs do not encourage development with a massive number of unit tests. It became obvious that it is hard and unnatural to use TDD in a framework where everything is tightly coupled with an ORM and as a consequence, with a database.

To be able to truly leverage the power of automated testing a very different approach is needed. One of them is called the _Clean Architecture_, where testability is one of the biggest advantages.

## Bibliography
1. Maciej Polańczyk _The Measurable Benefits of Unit Testing_ https://stxnext.com/blog/2017/11/02/measurable-benefits-unit-testing/
2. Ham Vocke _Practical Test Pyramid_ https://martinfowler.com/articles/practical-test-pyramid.html
3. Alister Scott _Testing Pyramids & Ice-Cream Cones_ https://watirmelon.blog/testing-pyramids/
4. Sebastian Buczyński - _How Can Your Software Benefit From Automated Testing?_ https://stxnext.com/blog/2017/08/09/how-can-your-software-benefit-automated-testing/
5. Kent Beck - _Test Driven Development: By Example_
6. Mary Poppendieck, Tom Poppendieck - _Leading Lean Software Development: Results are not the point_
7. pytest-profiling https://pypi.org/project/pytest-profiling/
8. snakeviz - https://jiffyclub.github.io/snakeviz/
