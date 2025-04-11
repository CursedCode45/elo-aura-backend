def expected_score(rating_a: float, rating_b: float) -> float:
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_rating(person_1: float, person_2: float, did_person1_win: bool, k=32) -> tuple[float, float]:
    """
    rating_a: current rating of player A
    rating_b: current rating of player B
    score_a: actual score (1 = win, 0.5 = draw, 0 = loss for A)
    k: K-factor (how much rating change)
    """
    score_1 = 1
    score_2 = 0
    if not did_person1_win:
        score_1 = 0
        score_2 = 1

    expected_a = expected_score(person_1, person_2)
    new_rating_a = person_1 + k * (score_1 - expected_a)

    expected_b = expected_score(person_2, person_1)
    new_rating_b = person_2 + k * (score_2 - expected_b)
    return new_rating_a, new_rating_b


girl_images = [
    ['https://images.unsplash.com/photo-1464863979621-258859e62245?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Z2lybCUyMGltYWdlc3xlbnwwfHwwfHx8MA%3D%3D',
    'https://i.pinimg.com/736x/0b/db/c7/0bdbc7e1f21b705d25b7f81873810086.jpg'],

    ['https://nypost.com/wp-content/uploads/sites/2/2022/10/Credit_-Alexia.jpg',
    'https://assets.teenvogue.com/photos/598cb013570d6e7387abfb11/16:9/w_2240,c_limit/DCe1LIcV0AAKKeP.jpg'],

    ['https://www.boredpanda.com/blog/wp-content/uploads/2020/05/woman-tinder-shamed-dress-asos-response-5-5eb1550d91797__700.jpg',
    'https://thepinknews.com/wp-content/uploads/images/2018/04/Alison-Tinder-650x650.jpg'],

    ['https://cdn.vox-cdn.com/thumbor/FOrU67HxxRcYiZSphucBGAnMLxw=/253x0:3558x2479/1200x675/filters:focal(253x0:3558x2479)/cdn.vox-cdn.com/uploads/chorus_image/image/45949834/Racked111.0.0.jpg',
    'https://i2-prod.plymouthherald.co.uk/news/local-news/article1415877.ece/ALTERNATES/s615b/tinder2.jpg'],

    ['https://www.perfocal.com/blog/content/images/2021/01/Perfocal_17-11-2019_TYWFAQ_100_standard-3.jpg',
    'https://nypost.com/wp-content/uploads/sites/2/2020/01/tinder-life-save-26.jpg?quality=75&strip=all']
]