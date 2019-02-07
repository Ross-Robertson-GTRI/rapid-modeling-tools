import json
import tempfile
import unittest
import warnings
from pathlib import Path

import pandas as pd

from graph_analysis.graph_creation import Evaluator, Manager, MDTranslator
from graph_analysis.graph_objects import DiEdge, PropertyDiGraph, Vertex
from graph_analysis.utils import object_dict_view

from . import DATA_DIRECTORY, OUTPUT_DIRECTORY, PATTERNS


# class TestProduceJson(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_json_creation(self):
#         manager = Manager(
#             excel_path=[DATA_DIRECTORY / 'Sample Equations.xlsx'],
#             json_path=PATTERNS / 'Parametric.json'
#         )
#         translator = manager.translator
#         evaluator = manager.evaluators[0]
#         evaluator.rename_df_columns()
#         evaluator.add_missing_columns()
#         evaluator.to_property_di_graph()
#         property_di_graph = evaluator.prop_di_graph
#         property_di_graph.create_vertex_set(
#             df=evaluator.df, translator=translator)
#         vert_set = property_di_graph.vertex_set
#         json_out = {'modification targets': []}
#         decs_json = []
#         edge_json = []
#         for vertex in vert_set:
#             vert_uml, decs_uml, edge_uml = vertex.create_node_to_uml(
#                 translator=translator)
#             json_out['modification targets'].extend(vert_uml)
#             decs_json.extend(decs_uml)
#             edge_json.extend(edge_uml)
#
#         json_out['modification targets'].extend(decs_json)
#         json_out['modification targets'].extend(edge_json)
#
#         (OUTPUT_DIRECTORY / 'changes_uml.json').write_text(
#             json.dumps(json_out, indent=4, sort_keys=True)
#         )
#
#     def test_change_excel_json_creation(self):
#         excel_files = [
#             DATA_DIRECTORY / 'Composition Example Model Baseline.xlsx',
#             DATA_DIRECTORY / 'Composition Example Model Changed.xlsx']
#         manager = Manager(excel_path=excel_files,
#                           json_path=PATTERNS / 'Composition.json'
#                           )
#
#         translator = manager.translator
#         for evaluator in manager.evaluators:
#             evaluator.rename_df_columns()
#             evaluator.add_missing_columns()
#             evaluator.to_property_di_graph()
#             property_di_graph = evaluator.prop_di_graph
#             property_di_graph.create_vertex_set(
#                 df=evaluator.df, translator=translator)
#             property_di_graph.create_edge_set()
#             vertex_set = property_di_graph.vertex_set
#
#         manager.get_pattern_graph_diff()
#         manager.changes_to_excel()
#
#     def test_composition_2_json(self):
#         manager = Manager(excel_path=[
#             DATA_DIRECTORY / 'Composition Example 2.xlsx'],
#             json_path=PATTERNS / 'Composition.json')
#         translator = manager.translator
#         evaluator = manager.evaluators[0]
#         evaluator.rename_df_columns()
#         evaluator.add_missing_columns()
#         evaluator.to_property_di_graph()
#         property_di_graph = evaluator.prop_di_graph
#         property_di_graph.create_vertex_set(
#             df=evaluator.df, translator=translator)
#         vert_set = property_di_graph.vertex_set
#         json_out = {'modification targets': []}
#         decs_json = []
#         edge_json = []
#         for vertex in vert_set:
#             vert_uml, decs_uml, edge_uml = vertex.create_node_to_uml(
#                 translator=translator)
#             json_out['modification targets'].extend(vert_uml)
#             decs_json.extend(decs_uml)
#             edge_json.extend(edge_uml)
#
#         (OUTPUT_DIRECTORY / 'composition_example_2_uml.json').write_text(
#             json.dumps(json_out, indent=4, sort_keys=True)
#         )
#
#     def test_change_composition_2_excel_json_creation(self):
#         original_file = 'Composition Example 2 Model Baseline.xlsx'
#         change_file = 'Composition Example 2 Model Changed.xlsx'
#         excel_files = [DATA_DIRECTORY / original_file,
#                        DATA_DIRECTORY / change_file]
#         manager = Manager(excel_path=excel_files,
#                           json_path=PATTERNS / 'Composition.json'
#                           )
#
#         translator = manager.translator
#         for evaluator in manager.evaluators:
#             evaluator.rename_df_columns()
#             evaluator.add_missing_columns()
#             evaluator.to_property_di_graph()
#             property_di_graph = evaluator.prop_di_graph
#             property_di_graph.create_vertex_set(
#                 df=evaluator.df, translator=translator)
#             property_di_graph.create_edge_set()
#             vertex_set = property_di_graph.vertex_set
#
#         manager.get_pattern_graph_diff()
#         manager.changes_to_excel()
#
#     def tearDown(self):
#         pass


class TestManager(unittest.TestCase):

    def setUp(self):
        pass
        # instead of making objects that go through all these tests
        # make the data the instance variables that I can access to make
        # instances of the classes locally within the function scope.
        # self.manager = Manager(
        #     excel_path=[
        #         DATA_DIRECTORY / 'Composition Example.xlsx'
        #         for i in range(2)],
        #     json_path=PATTERNS / 'Composition.json')

    def test_ids_assinged_in_change(self):
        manager = Manager(
            excel_path=[
                (DATA_DIRECTORY / 'Composition Example 2 Model Baseline.xlsx'),
                (DATA_DIRECTORY / 'Composition Example 2 Model Changed.xlsx')
            ],
            json_path=PATTERNS / 'Composition.json'
        )
        eval_base = manager.evaluators[0]
        # print(
        # eval_base.translator.uml_id['Miniature Inertial Measurement Unit'])
        # self.assertTrue(False)
        eval_change = manager.evaluators[1]
        # self.assertEqual(eval_base.excel_file.name,
        #                  'Composition Example 2 Model Baseline.xlsx')
        # self.assertEqual(eval_change.excel_file.name,
        #                  'Composition Example 2 Model Changed.xlsx')
        # print('baseline ids len = {0}'.format(
        #     len(eval_base.translator.uml_id.keys())))
        # print('change ids len = {0}'.format(
        #     len(eval_change.translator.uml_id.keys())
        # ))
        # base_key_set = set(eval_base.translator.uml_id.keys())
        # change_key_set = set(eval_change.translator.uml_id.keys())
        # key_difference = change_key_set.difference(base_key_set)
        # print(change_key_set.difference(base_key_set))
        # eval_change.sheets_to_dataframe(excel_file=eval_change.excel_file)
        # print(change_key_set.difference(base_key_set))
        # new_name_dict = eval_change.df_renames.to_dict(orient='list')
        # # print(new_name_dict)
        # new_to_old = {}
        # for count, val in enumerate(new_name_dict['new name']):
        #     new_to_old[val] = new_name_dict['old name'][count]
        # # print(new_to_old)
        # c_tran = eval_change.translator
        # for key, value in new_to_old.items():
        #     old_id = c_tran.get_uml_id(name=value)
        #     new_id = c_tran.get_uml_id(name=key)
        #     print('prior to updating dict')
        #     print('new: {0}, old: {1}'.format(new_id, old_id))
        #     c_tran.uml_id.update({
        #         key: old_id
        #     })
        #     new_id_2 = c_tran.get_uml_id(name=key)
        #     print('post updating dict')
        #     print('new: {0}, old: {1}'.format(new_id, old_id))

        eval_base.rename_df_columns()
        eval_base.add_missing_columns()
        eval_base.to_property_di_graph()
        base_prop_graph = eval_base.prop_di_graph
        base_prop_graph.create_vertex_set(
            df=eval_base.df, translator=eval_base.translator,
        )
        base_prop_graph.create_edge_set()
        base_vert_set = base_prop_graph.vertex_set
        base_vert_dict = base_prop_graph.vertex_dict
        eval_change.rename_df_columns()
        eval_change.add_missing_columns()
        eval_change.to_property_di_graph()
        change_prop_graph = eval_change.prop_di_graph
        change_prop_graph.create_vertex_set(
            df=eval_change.df, translator=eval_change.translator,
        )
        change_prop_graph.create_edge_set()
        change_vert_set = change_prop_graph.vertex_set
        change_vert_dict = change_prop_graph.vertex_dict
        # I want to see if the nodes in the graph have the right ids
        print(set(change_prop_graph).difference(set(base_prop_graph)))
        diff_nodes = set(change_prop_graph).difference(set(base_prop_graph))
        diff_dict = {key: eval_change.translator.uml_id[key]
                     for key in diff_nodes}
        print(diff_dict)
        print(change_vert_dict['Miniature Inertial Measurement Unit'])
        # manager.get_pattern_graph_diff(out_directory=DATA_DIRECTORY)
        # print(eval_change.translator.uml_id['new_2'])
        for key, value in eval_change.translator.uml_id.items():
            if key == 'count':
                continue
            if 'new' in value:
                print(key, value)
        self.assertTrue(False)

    def test_get_json_data(self):
        manager = Manager(
            excel_path=[
                DATA_DIRECTORY / 'Composition Example.xlsx'
                for i in range(2)],
            json_path=PATTERNS / 'Composition.json')
        expected_keys = ['Columns to Navigation Map',
                         'Pattern Graph Vertices',
                         'Pattern Graph Edge Labels',
                         'Pattern Graph Edges',
                         'Pattern Spanning Tree Edges',
                         'Pattern Spanning Tree Edge Labels',
                         'Root Node',
                         'Vertex MetaTypes',
                         'Vertex Stereotypes',
                         'Vertex Settings']

        self.assertListEqual(expected_keys, list(
            manager.json_data.keys()))

    def test_create_evaluators(self):
        manager = Manager(
            excel_path=[
                DATA_DIRECTORY / 'Composition Example.xlsx'
                for i in range(2)],
            json_path=PATTERNS / 'Composition.json')
        # weak test: create_evaluators() run during init
        self.assertEqual(2, len(manager.evaluators))
        for eval in manager.evaluators:
            self.assertIsInstance(eval, Evaluator)

    def test_get_pattern_graph_diff(self):
        # this is a bad function and an improper test.
        # The test ignores the obvious problem of non-unique matchings
        manager = Manager(
            excel_path=[
                DATA_DIRECTORY / 'Composition Example.xlsx'
                for i in range(2)],
            json_path=PATTERNS / 'Composition.json')
        base_inputs = [('s1', 't1', 'type'),
                       ('s12', 't12', 'memberEnd'),
                       ('song', 'tiger', 'blue'), ]
        base_df = pd.DataFrame(data={
            'source': ['s1', 's12', 'song'],
            'target': [edge[1] for edge in base_inputs],
            'type': ['type' for i in range(3)],
            'memberEnd': ['memberEnd' for i in range(3)],
            'blue': ['blue' for i in range(3)]
        })

        ancestor = [('as1', 't1', 'type'),
                    ('s12', 'at12', 'memberEnd'), ('b', 'c', 'orange')]

        base_edges = []
        base_vertex_dict = {}
        base_dict = {}
        ancestor_edges = []
        ancestor_vertex_dict = {}
        ancestor_dict = {}

        for edge_tuple in base_inputs:
            source = Vertex(name=edge_tuple[0],
                            node_types=['component'])
            target = Vertex(name=edge_tuple[1],
                            node_types=['Atomic Thing'])
            edge = DiEdge(source=source, target=target,
                          edge_attribute=edge_tuple[2])
            base_vertex_dict[edge_tuple[0]] = source
            base_vertex_dict[edge_tuple[1]] = target
            base_dict[edge_tuple] = edge
            base_edges.append(edge)

        for edge_tuple in ancestor:
            source = Vertex(name=edge_tuple[0],
                            node_types=['component'])
            target = Vertex(name=edge_tuple[1],
                            node_types=['Atomic Thing'])
            edge = DiEdge(source=source, target=target,
                          edge_attribute=edge_tuple[2])
            ancestor_vertex_dict[edge_tuple[0]] = source
            ancestor_vertex_dict[edge_tuple[1]] = target
            ancestor_dict[edge_tuple] = edge
            ancestor_edges.append(edge)

        manager.evaluators[0].df = base_df
        manager.evaluators[0].prop_di_graph = PropertyDiGraph()
        manager.evaluators[1].prop_di_graph = PropertyDiGraph()
        manager.evaluators[0].prop_di_graph.edge_set = set(base_edges)
        manager.evaluators[1].prop_di_graph.edge_set = set(ancestor_edges)
        manager.evaluators[0].prop_di_graph.vertex_dict = base_vertex_dict
        manager.evaluators[1].prop_di_graph.vertex_dict = ancestor_vertex_dict
        manager.evaluators[0].prop_di_graph.edge_dict = base_dict
        manager.evaluators[1].prop_di_graph.edge_dict = ancestor_dict
        df_data = {'new name': ['at12'],
                   'old name': ['t12']}
        manager.evaluators[1].df_renames = pd.DataFrame(data=df_data)
        self.assertTrue(manager.evaluators[1].has_rename)

        match_dict = manager.get_pattern_graph_diff()

        match_dict_str = {}
        added_to_str = []
        deleted_to_str = []
        add_del = ('Added', 'Deleted')
        for key in match_dict['0-1']['Changes']:
            if isinstance(key, str):
                if key in add_del:
                    match_dict_str.update({key:
                                           [value.named_edge_triple
                                            for value in match_dict[
                                                '0-1']['Changes'][key]]})
                    continue
                else:
                    vals = []
                    for value in match_dict['0-1']['Changes'][key]:
                        vals.append(value.name)
                    match_dict_str.update({key: vals})
            else:
                match_dict_str.update({key.named_edge_triple:
                                       match_dict[
                                           '0-1'][
                                           'Changes'][
                                           key][0].named_edge_triple})

        expected_matches = {('s1', 't1', 'type'): ('as1', 't1', 'type'),
                            'Rename new name': ['at12'],
                            'Rename old name': ['t12'],
                            'Added': [('b', 'c', 'orange'), ],
                            'Deleted': [('song', 'tiger', 'blue'), ], }
        self.assertDictEqual(expected_matches, match_dict_str)

    def test_changes_to_excel(self):
        manager = Manager(
            excel_path=[
                DATA_DIRECTORY / 'Composition Example.xlsx'
                for i in range(1)],
            json_path=PATTERNS / 'Composition.json')
        og_edge = DiEdge(source=Vertex(name='green'),
                         target=Vertex(name='apple'),
                         edge_attribute='fruit')
        change_edge = DiEdge(source=Vertex(name='gala'),
                             target=Vertex(name='apple'),
                             edge_attribute='fruit')
        added_edge = DiEdge(source=Vertex(name='blueberry'),
                            target=Vertex(name='berry'),
                            edge_attribute='bush')
        deleted_edge = DiEdge(source=Vertex(name='yellow'),
                              target=Vertex(name='delicious'),
                              edge_attribute='apple')
        unstable_key = DiEdge(source=Vertex(name='tomato'),
                              target=Vertex(name='fruit'),
                              edge_attribute='fruit')
        unstable_one = DiEdge(source=Vertex(name='tomato'),
                              target=Vertex(name='vegetable'),
                              edge_attribute='fruit')
        unstable_two = DiEdge(source=Vertex(name='tomahto'),
                              target=Vertex(name='fruit'),
                              edge_attribute='fruit')
        new_name = Vertex(name='new name')
        old_name = Vertex(name='old name')

        fake_datas = {'0-1': {'Changes': {'Added': [added_edge],
                                          'Deleted': [deleted_edge],
                                          og_edge: [change_edge],
                                          'Rename new name': [new_name],
                                          'Rename old name': [old_name], },
                              'Unstable Pairs': {unstable_key: [
                                  unstable_one,
                                  unstable_two]}}}
        manager.evaluator_change_dict = fake_datas
        with tempfile.TemporaryDirectory() as tmpdir:
            outdir = Path(tmpdir)
            manager.changes_to_excel(out_directory=outdir)

            created_file_name = list(outdir.glob('*.xlsx'))[0]
            created_file = OUTPUT_DIRECTORY / created_file_name
            created_df = pd.read_excel(created_file)
            created_dict = created_df.to_dict()

            expected_data = {'Edit 1': ["('green', 'apple', 'fruit')",
                                        "('tomato', 'fruit', 'fruit')",
                                        "('tomato', 'fruit', 'fruit')", ],
                             'Edit 2': ["('gala', 'apple', 'fruit')",
                                        "('tomato', 'vegetable', 'fruit')",
                                        "('tomahto', 'fruit', 'fruit')", ],
                             'Added': ["('blueberry', 'berry', 'bush')"],
                             'Deleted': ["('yellow', 'delicious', 'apple')"],
                             'Rename new name': ["new name"],
                             'Rename old name': ["old name"], }

            expected_df = pd.DataFrame(data=dict([
                (k, pd.Series(v)) for k, v in expected_data.items()]))
            expected_dict = expected_df.to_dict()
            self.assertDictEqual(expected_dict, created_dict)
            self.assertTrue(expected_df.equals(created_df))

    def test_graph_difference_to_json_2(self):
        manager = Manager(
            excel_path=[
                (DATA_DIRECTORY / 'Composition_Diff_JSON_Baseline.xlsx'),
                (DATA_DIRECTORY / 'Composition_Diff_JSON_Changed.xlsx'),
            ],
            json_path=PATTERNS / 'Composition.json'
        )
        tr = manager.translator
        print(manager.evaluators)
        eval = manager.evaluators[0]
        eval1 = manager.evaluators[-1]
        eval.rename_df_columns()
        eval.add_missing_columns()
        eval.to_property_di_graph()
        pdg = eval.prop_di_graph
        pdg.create_vertex_set(
            df=eval.df, translator=eval.translator
        )
        pdg.create_edge_set()
        vset = pdg.vertex_set
        e_set = pdg.edge_set

        eval1.rename_df_columns()
        eval1.add_missing_columns()
        eval1.to_property_di_graph()
        pdg1 = eval1.prop_di_graph
        pdg1.create_vertex_set(
            df=eval1.df, translator=eval1.translator
        )
        pdg1.create_edge_set()
        vset1 = pdg.vertex_set
        e_set1 = pdg1.edge_set

        print('the edge set of baseline')
        e = {edge.named_edge_triple: edge
             for edge in e_set}
        print(sorted(e.keys(), key=lambda elem: elem[0]))
        print('the edge set of changed')
        ec = {edge.named_edge_triple: edge
              for edge in e_set1}
        print(sorted(ec.keys(), key=lambda elem: elem[0]))

        change_dict = manager.get_pattern_graph_diff(
            out_directory=DATA_DIRECTORY)
        print(change_dict)
        manager.changes_to_excel(out_directory=DATA_DIRECTORY)
        print('print statement here')
        self.assertTrue(False)

    def test_graph_difference_to_json(self):
        manager = Manager(
            excel_path=[
                DATA_DIRECTORY / 'Composition Example.xlsx'
                for i in range(2)],
            json_path=PATTERNS / 'Composition.json')
        tr = manager.translator

        base_inputs = [('s1', 't1', 'type'),
                       ('s12', 't12', 'memberEnd'),
                       ('song', 'tiger', 'blue'), ]

        base_df = pd.DataFrame(data={
            'source': ['s1', 's12', 'song'],
            'target': [edge[1] for edge in base_inputs],
            'type': ['type' for i in range(3)],
            'memberEnd': ['memberEnd' for i in range(3)],
            'blue': ['blue' for i in range(3)]
        })

        ancestor = [('as1', 't1', 'type'),
                    ('s12', 'at12', 'memberEnd'),
                    ('b', 'c', 'orange'), ]

        base_edges = []
        base_dict = {}
        ancestor_edges = []
        ancestor_dict = {}

        for edge_tuple in base_inputs:
            source = Vertex(name=edge_tuple[0],
                            node_types=['component'])
            target = Vertex(name=edge_tuple[1],
                            node_types=['Atomic Thing'])
            edge = DiEdge(source=source, target=target,
                          edge_attribute=edge_tuple[2])
            tr.get_uml_id(name=edge_tuple[0])
            tr.get_uml_id(name=edge_tuple[1])
            base_dict[edge_tuple] = edge
            base_edges.append(edge)

        for edge_tuple in ancestor:
            source = Vertex(name=edge_tuple[0],
                            node_types=['component'])
            target = Vertex(name=edge_tuple[1],
                            node_types=['Atomic Thing'])
            edge = DiEdge(source=source, target=target,
                          edge_attribute=edge_tuple[2])
            tr.get_uml_id(name=edge_tuple[0])
            tr.get_uml_id(name=edge_tuple[1])
            ancestor_dict[edge_tuple] = edge
            ancestor_edges.append(edge)

        base_edge = base_dict[('s1', 't1', 'type')]
        ances_edge = ancestor_dict[('as1', 't1', 'type')]
        at12 = ancestor_dict[('s12', 'at12', 'memberEnd')].target
        t12 = base_dict[('s12', 't12', 'memberEnd')].target
        add_edge = ancestor_dict[('b', 'c', 'orange')]
        del_edge = base_dict[('song', 'tiger', 'blue')]

        change_dict = {base_edge: [ances_edge, ],
                       'Rename new name': [at12, ],
                       'Rename old name': [t12, ],
                       'Added': [add_edge, ],
                       'Deleted': [del_edge, ], }
        cd = change_dict
        desired = [ances_edge.source.create_node_to_uml(translator=tr)[0][0],
                   base_edge.edge_to_uml(op='delete', translator=tr),
                   cd['Deleted'][0].edge_to_uml(op='delete', translator=tr),
                   ances_edge.edge_to_uml(op='replace', translator=tr),
                   cd['Added'][0].edge_to_uml(op='replace', translator=tr),
                   cd['Rename new name'][0].change_node_to_uml(translator=tr),
                   ]

        changes = manager.graph_difference_to_json(new_col='Rename new name',
                                                   change_dict=change_dict,
                                                   evaluators='0-1',
                                                   translator=tr)

        # THis test is super sensitive to the order the IDs are created above
        # a better way around this would be to assign bs ids manually and
        # the one id that says 'new_1' for as1 to make sure it goes through the
        # correct channels.
        for count, change in enumerate(changes):
            if isinstance(change, tuple) and isinstance(desired[count], tuple):
                self.assertTupleEqual(desired[count], change)
            else:
                self.assertDictEqual(desired[count], change)

    def tearDown(self):
        pass


class TestEvaluator(unittest.TestCase):
    # TODO: Make sure all additional graph objects that are desired are
    # created by the graph creation logic.
    # TODO: Test the PROCESS of some of these functions.

    def setUp(self):
        data = (PATTERNS / 'Composition.json').read_text(
        )
        data = json.loads(data)

        self.translator = MDTranslator(json_data=data)
        self.evaluator = Evaluator(
            excel_file=DATA_DIRECTORY / 'Composition Example.xlsx',
            translator=self.translator)

        data_dict = {
            'Component': ['Car', 'Car', 'Car', 'Car', 'Car', 'Car',
                          'Car', 'Wheel', 'Wheel', 'Wheel', 'Engine',
                          'Engine', 'Engine', 'Engine', 'Engine', 'Engine', ],
            'Position': ['engine', 'chassis', 'driveshaft', 'front passenger',
                         'front driver', 'rear passenger', 'rear driver',
                         'hub', 'tire', 'lug nut', 'one', 'two', 'three',
                         'four', 'drive output', 'mount'],
            'Part': ['Engine', 'Chassis', 'Driveshaft', 'Wheel', 'Wheel',
                     'Wheel', 'Wheel', 'Hub', 'Tire', 'Lug Nut', 'Cylinder',
                     'Cylinder', 'Cylinder', 'Cylinder', 'Drive Output',
                     'Mount']
        }
        self.evaluator.df = pd.DataFrame(data=data_dict)

    def test_sheets_to_dataframe(self):
        data = (PATTERNS / 'Composition.json').read_text(
        )
        data = json.loads(data)

        ex_f = DATA_DIRECTORY / 'Composition Example Model Baseline.xlsx'
        translator = MDTranslator(json_data=data)
        evaluator = Evaluator(
            excel_file=ex_f,
            translator=translator
        )
        file_name = 'Composition Example Model Baseline.xlsx'
        evaluator.sheets_to_dataframe(excel_file=DATA_DIRECTORY / file_name)
        columns_list = [col for col in evaluator.df.columns]
        self.assertListEqual(
            ['Component', 'Position', 'Part'], columns_list)

        # 63 ids provided .
        self.assertEqual(63, len(evaluator.df_ids))

    def test_has_rename(self):
        data = (PATTERNS / 'Composition.json').read_text(
        )
        data = json.loads(data)

        translator = MDTranslator(json_data=data)
        excel_file = DATA_DIRECTORY / 'Composition Example Model Changed.xlsx'
        evaluator = Evaluator(
            excel_file=excel_file,
            translator=translator
        )
        self.assertTrue(evaluator.has_rename)
        excel_no_rename = (
            DATA_DIRECTORY / 'Composition Example Model Baseline.xlsx')
        evaluator_no_rename = Evaluator(
            excel_file=excel_no_rename,
            translator=translator
        )
        self.assertFalse(evaluator_no_rename.has_rename)

    def test_rename_df_columns(self):
        # just need to test that the columns are as expected.
        # utils tests the two auxillary functions that rename df entries.
        expected_cols = ['Composite Thing',
                         'component',
                         'Atomic Thing',
                         ]
        self.evaluator.rename_df_columns()
        self.assertListEqual(expected_cols, list(self.evaluator.df.columns))
        self.assertEqual(set(), self.evaluator.root_node_attr_columns)

    def test_add_missing_columns(self):
        # TODO: explicitly check that the new columns are made.
        # TODO: remove reliance on excelfile data.
        # TODO: This is an incomplete test because it does not test for
        # the case of no space column to be created.
        evaluator = Evaluator(
            excel_file=DATA_DIRECTORY / 'Composition Example.xlsx',
            translator=self.translator)
        evaluator.translator.get_pattern_graph().append('cardinal')
        evaluator.translator.get_pattern_graph().append('component context')
        evaluator.translator.get_pattern_graph().append(
            'A_composite owner_component-end1'
        )
        # self.assertTrue(False, msg='Extend this to get the if case in space')
        data_dict = {
            'Composite Thing': ['Car', 'Wheel', 'Engine'],
            'component': ['chassis', 'tire', 'mount'],
            'Atomic Thing': ['Chassis', 'Tire', 'Mount']
        }
        df = pd.DataFrame(data=data_dict)
        evaluator.df = df
        evaluator.rename_df_columns()
        expected_cols = {'Composite Thing',
                         'component',
                         'Atomic Thing',
                         'composite owner',
                         'A_composite owner_component',
                         'cardinal',
                         'component context',
                         'A_composite owner_component-end1', }
        evaluator.add_missing_columns()

        self.assertSetEqual(expected_cols, set(evaluator.df.columns))

        expected_composite_owner = ['car qua chassis context',
                                    'wheel qua tire context',
                                    'engine qua mount context']
        expected_comp_owner_comp = ['A_car qua chassis context_chassis',
                                    'A_wheel qua tire context_tire',
                                    'A_engine qua mount context_mount']
        expect_cardinal = ['car cardinal', 'wheel cardinal',
                           'engine cardinal']
        expect_space_in_df = ['chassis qua context context',
                              'tire qua context context',
                              'mount qua context context']
        expect_dash = ['A_car qua chassis context_chassis-end1',
                       'A_wheel qua tire context_tire-end1',
                       'A_engine qua mount context_mount-end1']
        self.assertListEqual(expected_composite_owner,
                             list(evaluator.df['composite owner']))
        self.assertListEqual(expected_comp_owner_comp,
                             list(evaluator.df[
                                 'A_composite owner_component']))
        self.assertListEqual(expect_cardinal,
                             list(evaluator.df['cardinal']))
        self.assertListEqual(expect_space_in_df,
                             list(evaluator.df['component context']))
        self.assertListEqual(expect_dash,
                             list(evaluator.df[
                                 'A_composite owner_component-end1']))

    def test_to_property_di_graph(self):
        # the goal is to create a graph object.
        # networkx provides the functionality to get the data into the graph
        # the graph itself will be tested so I should just test that a graph
        # obj exists.
        # self.evaluator.rename_df_columns()
        # self.evaluator.add_missing_columns()
        # self.evaluator.to_property_di_graph()
        # self.assertTrue(self.evaluator.prop_di_graph)
        # self.assertIsInstance(self.evaluator.prop_di_graph,
        #                       PropertyDiGraph)

        # TODO: create tests for the properties on the Evaluator class.
        data_dict = {
            'Composite Thing': ['blueberry', ],
            'component': ['pie', ],
            'Atomic Thing': ['milk']
        }
        data_id_dict = {
            'Element Names': ['blueberry', 'pie', 'milk'],
            'ID': [123, 234, 345]
        }
        evaluator = Evaluator(excel_file=(
            DATA_DIRECTORY / 'Composition Example Model Baseline.xlsx'),
            translator=self.translator)
        evaluator.df = pd.DataFrame(data=data_dict)
        df_ids = pd.DataFrame(data=data_id_dict)
        df_ids.set_index(df_ids.columns[0], inplace=True)
        evaluator.df_ids = df_ids
        evaluator.translator.uml_id.update(
            evaluator.df_ids.to_dict(
                orient='dict')[evaluator.df_ids.columns[0]]
        )
        evaluator.rename_df_columns()
        evaluator.add_missing_columns()
        evaluator.to_property_di_graph()

        graph_node_data = list(evaluator.prop_di_graph.nodes().data())
        expected_node_ids = [('blueberry qua pie context', {'ID': 'new_0'}),
                             ('blueberry', {'ID': 123}),
                             ('pie', {'ID': 234}),
                             ('milk', {'ID': 345}),
                             ('A_blueberry qua pie context_pie',
                              {'ID': 'new_1'})]

        self.assertListEqual(expected_node_ids, graph_node_data)

    def tearDown(self):
        pass


class TestMDTranslator(unittest.TestCase):

    def setUp(self):
        # TODO: Note that this relies on Composition.json
        data = (PATTERNS / 'Composition.json').read_text()
        data = json.loads(data)

        self.translator = MDTranslator(json_data=data)

    def test_get_root_node(self):
        root_node = 'component'
        self.assertEqual(root_node, self.translator.get_root_node())

    def test_get_cols_to_nav_map(self):
        cols_to_nav = ['Component', 'Position', 'Part']
        self.assertListEqual(
            cols_to_nav, list(self.translator.get_cols_to_nav_map().keys()))

    def test_get_pattern_graph(self):
        pattern_graph = ['Composite Thing',
                         'Atomic Thing',
                         'A_composite owner_component',
                         'composite owner',
                         'component']
        self.assertListEqual(pattern_graph,
                             self.translator.get_pattern_graph())

    def test_get_pattern_graph_edges(self):
        node_pairs_list = self.translator.get_pattern_graph_edges()
        self.assertEqual(6, len(node_pairs_list))

    def test_get_edge_type(self):
        self.assertEqual('type', self.translator.get_edge_type(index=0))

    def test_get_uml_metatype(self):
        metatype = self.translator.get_uml_metatype(
            node_key='Composite Thing')
        self.assertEqual('Class', metatype)

    def test_get_uml_stereotype(self):
        stereotype = self.translator.get_uml_stereotype(
            node_key='Composite Thing'
        )
        self.assertEqual('Block', stereotype)

        stereotype_2 = self.translator.get_uml_stereotype(
            node_key='composite owner'
        )
        self.assertEqual(None, stereotype_2)

    def test_get_uml_settings(self):
        path, setting = self.translator.get_uml_settings(
            node_key='Composite Thing'
        )
        self.assertTupleEqual(('Composite Thing', None), (path, setting))

        path_comp, setting_comp = self.translator.get_uml_settings(
            node_key='component'
        )
        self.assertEqual(('aggregation', 'composite'),
                         (path_comp, setting_comp))

    def tearDown(self):
        pass
