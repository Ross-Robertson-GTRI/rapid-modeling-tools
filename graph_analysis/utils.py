import json
import os

from itertools import count
from random import shuffle


UML_ID = {
    'count': 0
}


def get_uml_id(name=None):
    """Returns the UML_ID for the corresponding vertex name provided. If the
    name provided does not exist as a key in the UML_ID dictionary than a
    new key is created using that name and the value increments with
    new_<ith new number>.

    Parameters
    ----------
    name : string
        The Vertex.name attribute

    Notes
    -----
    This will be updated to become a nested dictionary
    with the first key being the name and the inner key will be the
    new_<ith new number> key and the value behind that will be the UUID created
    by MagicDraw.
    """
    # TODO: make this a generator function
    if name in UML_ID.keys():
        return UML_ID[name]
    else:
        UML_ID.update({name: 'new_{0}'.format(UML_ID['count'])})
        UML_ID['count'] += 1
        return UML_ID[name]


def create_column_values_under(prefix=None,
                               first_node_data=None,
                               second_node_data=None,
                               suffix=''):
    """Returns the column values for an inferred dataframe column that has
    underscores in the column name.

    Parameters
    ----------
    prefix : string
        the characters that appear in the column name before the first '_'

    first_node_data : list
        List of data with a length equal to the number of rows in the dataframe
        determined by picking the dataframe column with the same name as the
        string between the first underscore and the second.

    second_node_data : list
        List of data with a length equal to the number of rows in the dataframe
        determined by picking the dataframe column with the same name as the
        string after the second underscore.

    suffix : string
        If the inferred column name contained a '-' followed by additional
        characters then those are treated as the suffix. Otherwise, it
        initalizes the the empty string and does nothing.

    Notes
    -----
    This function expects to receive a string like
    'A_composite owner_component-end1' with prefix=A,
    first_node_data=df['composite owner'], second_node_data=df['component'],
    and suffix='-end1'
    To produce the dataframe entires of the form:
    df['A_composite owner_component'] = A_<composite owner>_<component>
    """
    under = '_'
    dash = '-'
    column_values = []
    for count, first_data in enumerate(first_node_data):
        tmp_list = [prefix
                    + under
                    + first_data.lower()
                    + under
                    + second_node_data[count].lower()
                    + suffix
                    ]

        column_values.extend(tmp_list)

    return column_values


def create_column_values_space(first_node_data=None,
                               second_node_data=None):
    """Returns the column values for an inferred dataframe column that has
    spaces in the column name.

    Parameters
    ----------
    first_node_data : list
        List of data with a length equal to the number of rows in the dataframe
        determined by picking the first dataframe column. This will change
        once a more appropriate rule has been decided.

    second_node_data : list
        List of data with a length equal to the number of rows in the dataframe
        determined by picking the dataframe column with the same name as the
        string after the space.

    Notes
    -----
    Up stream in the Evaluator.add_missing_columns() method, the Evaluator
    assumes that the first_node_data should come from the first column in the
    dataframe however, that can change and this function will be unaffected.
    If the first_node_data='CAR' and the second_node_data='BOOT' then the
    value returned would be 'car qua boot context'
    """
    space = ' '
    column_values = []
    for count, first_data in enumerate(first_node_data):
        tmp_list = [first_data.lower()
                    + space
                    + 'qua'
                    + space
                    + second_node_data[count].lower()
                    + space
                    + 'context'
                    ]
        column_values.extend(tmp_list)

    return column_values


def create_column_values_singleton(first_node_data=None,
                                   second_node_data=None):
    """Returns the column values for an inferred dataframe column that is only
    one word.

    Parameters
    ----------
    first_node_data : list
        List of data with a length equal to the number of rows in the dataframe
        determined by picking the dataframe column corresponding to the
        root node. This may change once a more appropriate rule has been
        decided.

    second_node_data : list
        List of data with a length equal to the number of rows in the dataframe
        built by repeating the desired column name until it has
        the same length as first_node_data.

    Notes
    -----
    Up stream in the Evaluator.add_missing_columns() method, the Evaluator
    assumes that the first_node_data should come from the root node of the
    dataframe however, that can change and this function will be unaffected.
    Furthermore, the second_node_data may change but at this stage the values
    are determined as explained above.
    If the first_node_data='CAR' and the second_node_data='context1' then the
    value returned would be 'car context1'
    """
    space = ' '
    column_values = []
    for count, first_data in enumerate(first_node_data):
        tmp_list = [first_data.lower()
                    + space
                    + second_node_data[count].lower()
                    ]
        column_values.extend(tmp_list)

    return column_values


def create_column_values(col_name=None, data=None, aux_data=None):
    """Deprecated, I believe this may be removed without consequence."""
    column_values = []
    # check prefix for an underscore
    if '_' in col_name:
        # for the A_composite owner_component column and any with an _
        under = '_'
        chopped_str = col_name.split(sep='_')
        for count, item in enumerate(data):
            tmp_list = [chopped_str[0]
                        + under
                        + item.lower()
                        + under
                        + aux_data[count]]
            column_values.extend(tmp_list)
        return column_values
    else:
        # for the composite owner column and i guess all others...
        space = ' '
        for count, item in enumerate(data):
            tmp_list = [item.lower()
                        + space
                        + 'qua'
                        + space
                        + aux_data[count].lower()
                        + space
                        + 'context']
            column_values.extend(tmp_list)
        return column_values


def get_node_types_attrs(df=None, node=None,
                         root_node_type=None, root_attr_columns=None):
    """Returns the type of node that specified vertex is acting as and
    returns the attributes associated with that node if the passed node is
    a root node.

    Parameters
    ----------
    df : Pandas DataFrame
        The DataFrame that is read in from Excel and that creates the Graph.

    node : string
        The name of the graph vertex object that the node_types should be
        associated with.

    root_node_type : string
        The name of the root node type, which is the same as the column
        header for the DataFrame and the value behind the rootNode key in the
        json file.

    root_attr_columns : list of dictionaries
        The list of dictionaries created form the additional columns present
        in the excel file that are not part of the 'Columns to Navigation
        Map' and that should be associated to a node if that node is a root
        node.
    """
    node_attr_dict = {}
    mask = df == node
    node_mask_columns = df[mask].dropna(axis=1, how='all').columns
    node_type_columns = set(node_mask_columns).difference(
        root_attr_columns)

    root_attribute_list = list(root_attr_columns)

    # want to check if node in root nodes.values the column not the attrs.
    if node in df[root_node_type].values:
        root_node_df = df.loc[df[root_node_type] == node]
        node_attr_dict = root_node_df[root_attribute_list].dropna(
            axis=1, how='all').dropna(axis=0, how='all').to_dict('records')

    return node_type_columns, node_attr_dict


def match_changes(change_dict=None, score=None, match_ancestors=None):
    count = 0
    unstable_pairing = {}
    if not score:
        score = {}
    if not match_ancestors:
        match_ancestors = {}

    # this is running a version of the stable marriage algorithm
    # suitors are keys in the change_dict looking for engagements to the
    # values they contian.
    add_del = ('Added', 'Deleted')
    for suitor in change_dict:
        # TODO: generalize key skip method
        if suitor in add_del or not change_dict[suitor]:
            if not change_dict[suitor] and suitor not in add_del:
                print(suitor)
                deleted_set = set(change_dict['Deleted']).add(suitor)
                update_dict = {'Deleted': deleted_set}
                change_dict.update(update_dict)
            count += 1
            continue

        if suitor not in score.keys():  # initialize a score
            preference = match(current=suitor, clone=change_dict[suitor][0])
            score[suitor] = preference
            match_ancestors.update({change_dict[suitor][0]: suitor})

        if len(change_dict[suitor]) > 1:  # loop over suitors for engagements
            preference = match(current=suitor, clone=change_dict[suitor][1])

            if preference > score[suitor]:  # match with node in 1th position
                if match_ancestors[change_dict[suitor][0]] == suitor:
                    match_ancestors.update({change_dict[suitor][0]: None})
                    # record how the values match to the keys.

                # remove previous engagement as more favorable pairing found
                change_dict[suitor].pop(0)
                score[suitor] = preference
                match_ancestors.update({change_dict[suitor][0]: suitor})
            elif preference < score[suitor]:  # do nothing 1th node less likely
                change_dict[suitor].pop(1)
            elif preference == score[suitor] and preference < 1:
                # because this is an imperfect application of stable marriage
                # when a favorable pariing is found but there are still suitors
                # in the list, shuffle the list to try to remove remaining
                score.pop(suitor, None)
                shuffle(change_dict[suitor])
            else:
                unstable_pairing.update({suitor: change_dict[suitor]})
                # at least two likely pairs but shuffle to try to reduce the
                # list to the minimal pairing.
                shuffle(change_dict[suitor])
                # could rerun the checks using the unstable pairing dict
                count += 1
        else:
            match_ancestors.update({change_dict[suitor][0]: suitor})
            count += 1

    if count == len(change_dict.keys()):
        return (change_dict, unstable_pairing, score)
    else:  # This function alone responsible for returning probably matchings
        return match_changes(change_dict=change_dict, score=score,
                             match_ancestors=match_ancestors)


def match(current=None, clone=None):
    # this function should only be getting nodes with the same edges
    # if I change this to assume nodes of the same edge attr then I can
    # send this function "equivalent edges"
    if current.edge_attribute == clone.edge_attribute:
        if ((current.source.name == clone.source.name)
                or (current.target.name == clone.target.name)):
            # TODO: check subgraph
            # if subgraph is isomorphic then return 2
            return 1
        else:
            return 0
    elif len(current.edge_attribute) > len(clone.edge_attribute):
        return -1
    else:  # edge attribute of current is shorter than of clone
        return -2


def associate_node_ids(nodes=None, attr_df=None, uml_id_dict=None):
    # return a list of tuples with (node name, {id: <node id>})
    # TODO: this function should do more. Need something for the else
    # otherwise this silently corrupts data.
    # This could be expanded to add attrs but its really only adding ids.
    nodes_to_add = []
    for node in nodes:
        if node in attr_df.index:
            attr = attr_df.loc[node].to_dict()
            nodes_to_add.append((node, attr))
        else:
            attr = {'ID': uml_id_dict(name=node)}
            nodes_to_add.append((node, attr))

    return nodes_to_add


def to_excel_df(data_dict=None, column_keys=None):
    # Idea: df_data = {'Edit 1': [keys for the changes], 'Edit 2': [values for
    # each key], 'Added': [all added data], 'Deleted': [all deleted data]
    df_data = {}
    for key in data_dict:
        if key in column_keys:
            df_data[key] = [val for val in data_dict[key]]

    pass


def object_dict_view(cipher=None):
    """ Just to make my life easier
    """
    decoded = {}
    for key in cipher.keys():
        if type(key) is str:
            decoded.update({key: [
                item.named_edge_triple for item in cipher[key]]})
        else:
            decoded.update({key.named_edge_triple:
                            [item.named_edge_triple
                             for item in cipher[key]]})

    return decoded


def get_setting_node_name_from_df(df=None, column=None, node=None):
    """Returns a list of nodes located under the double mask defined first by
    masking the dataframe for the particular node of interest and dropping all
    of the empty rows, then by pulling out the node names from non-empty rows
    that are not equal to the input node. In other words we want to find all of
    nodes related to ours for a particular node_type. Since we wanted to know
    all of the nodes related to the input node of a particular node type, this
    was believed to be better than searching the neghiborhood and throwing out
    any nodes that did not have the same typeself.

    Parameters
    ----------
    df : Pandas DataFrame
        The DataFrame that is read in from Excel and that creates the Graph.

    node : string
        The name of the graph vertex object that we are interested in locating
        the related nodes of, of a particular type.

    column : string
        The name of the column of interest that we are interested in.
        The name of that column was stript from a vertex settings key asking
        for an id<column name>.

    Notes
    -----
    This function returns a python list of names of nodes that are found in the
    dataframe under the column header 'column' and relating to the input
    node.
    """

    mask = df == node
    masked_df = df[mask].dropna(axis=0, how='all')
    return df.where(
        masked_df.isnull()).dropna(axis=0, how='all')[column].tolist()


def aggregate_change_json():
    pass
