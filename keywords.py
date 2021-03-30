from monkeylearn import MonkeyLearn


def get_keywords(data_):
    ml = MonkeyLearn('1c0950b2356a258e00b735ab4002679a9a1f3642')
    model_id = 'ex_YCya9nrn'
    result = ml.extractors.extract(model_id, data_)
    extraction = ''
    for ex in result.body[0]['extractions']:
        extraction += ex['parsed_value'] + " "
    return extraction.strip()
