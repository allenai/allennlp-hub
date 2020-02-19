from allennlp_hub.pretrained.helpers import _load_predictor
from allennlp_semparse import predictors as semparse_predictors
import allennlp_semparse.models
import allennlp_semparse.dataset_readers

# AllenNLP Semparse models


def wikitables_parser_dasigi_2019() -> semparse_predictors.WikiTablesParserPredictor:
    predictor = _load_predictor(
        "https://allennlp.s3.amazonaws.com/models/wikitables-model-2020.02.10.tar.gz",
        "wikitables-parser",
    )
    return predictor


def nlvr_parser_dasigi_2019() -> semparse_predictors.NlvrParserPredictor:
    predictor = _load_predictor(
        "https://allennlp.s3.amazonaws.com/models/nlvr-erm-model-2020.02.10-rule-vocabulary-updated.tar.gz",
        "nlvr-parser",
    )
    return predictor


def atis_parser_lin_2019() -> semparse_predictors.AtisParserPredictor:
    predictor = _load_predictor(
        "https://allennlp.s3.amazonaws.com/models/atis-parser-2020.02.10.tar.gz",
        "atis-parser",
    )
    return predictor

