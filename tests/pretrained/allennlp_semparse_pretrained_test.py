import pytest
import spacy

from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained


class AllenNlpSemparsePretrainedTest(AllenNlpTestCase):
    def test_wikitables_parser(self):
        predictor = pretrained.wikitables_parser_dasigi_2019()
        table = """#	Event Year	Season	Flag bearer
7	2012	Summer	Ele Opeloge
6	2008	Summer	Ele Opeloge
5	2004	Summer	Uati Maposua
4	2000	Summer	Pauga Lalau
3	1996	Summer	Bob Gasio
2	1988	Summer	Henry Smith
1	1984	Summer	Apelu Ioane"""
        question = "How many years were held in summer?"
        result = predictor.predict_json({"table": table, "question": question})
        assert result["answer"] == 7
        assert (
            result["logical_form"][0]
            == "(count (filter_in all_rows string_column:season string:summer))"
        )

    def test_nlvr_parser(self):
        predictor = pretrained.nlvr_parser_dasigi_2019()
        structured_rep = """[
            [
                {"y_loc":13,"type":"square","color":"Yellow","x_loc":13,"size":20},
                {"y_loc":20,"type":"triangle","color":"Yellow","x_loc":44,"size":30},
                {"y_loc":90,"type":"circle","color":"#0099ff","x_loc":52,"size":10}
            ],
            [
                {"y_loc":57,"type":"square","color":"Black","x_loc":17,"size":20},
                {"y_loc":30,"type":"circle","color":"#0099ff","x_loc":76,"size":10},
                {"y_loc":12,"type":"square","color":"Black","x_loc":35,"size":10}
            ],
            [
                {"y_loc":40,"type":"triangle","color":"#0099ff","x_loc":26,"size":20},
                {"y_loc":70,"type":"triangle","color":"Black","x_loc":70,"size":30},
                {"y_loc":19,"type":"square","color":"Black","x_loc":35,"size":10}
            ]
        ]"""
        sentence = "there is exactly one yellow object touching the edge"
        result = predictor.predict_json(
            {"structured_rep": structured_rep, "sentence": sentence}
        )
        assert result["denotations"][0] == ["False"]
        assert (
            result["logical_form"][0]
            == "(object_count_equals (yellow (touch_wall all_objects)) 1)"
        )

    def test_atis_parser(self):
        predictor = pretrained.atis_parser_lin_2019()
        utterance = "give me flights on american airlines from milwaukee to phoenix"
        result = predictor.predict_json({"utterance": utterance})
        predicted_sql_query = """
  (SELECT DISTINCT flight . flight_id
   FROM flight
   WHERE (flight . airline_code = 'AA'
          AND (flight . from_airport IN
                 (SELECT airport_service . airport_code
                  FROM airport_service
                  WHERE airport_service . city_code IN
                      (SELECT city . city_code
                       FROM city
                       WHERE city . city_name = 'MILWAUKEE' ) )
               AND flight . to_airport IN
                 (SELECT airport_service . airport_code
                  FROM airport_service
                  WHERE airport_service . city_code IN
                      (SELECT city . city_code
                       FROM city
                       WHERE city . city_name = 'PHOENIX' ) ))) ) ;"""
        assert result["predicted_sql_query"] == predicted_sql_query
