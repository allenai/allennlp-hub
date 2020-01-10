from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive


def _load_predictor(archive_file: str, predictor_name: str) -> Predictor:
    """
    Helper to load the desired predictor from the given archive.
    """
    archive = load_archive(archive_file)
    return Predictor.from_archive(archive, predictor_name)
