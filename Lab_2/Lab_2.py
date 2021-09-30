import networkx as nx
import matplotlib.pyplot as plt
# from check_deterministic import check_deterministic
def check_deterministic(graph: nx.DiGraph):
    """ Проверяет какой это автомат
        @:returns
            @rvalue = True  Детерменированный автомат
            @rvalue = False Недетерменированный автомат

        Я определяю это посредством просмотра условий перехода.
        Если из одной вершины с одинаковым условием выходит несколько рёбер
        - это недетерменированный автомат.
    """
    for key_begin in graph.adj.keys():
        weigths = []
        for key_end in graph.adj[key_begin].keys():
            weigths.append(graph.adj[key_begin][key_end]['weight'])
        if len(weigths) != len(set(weigths)):
            print("This is an Undetermined automaton!")
            return False
    print("This is an Determined automaton)")
    return True

# from draw import draw
def draw(graph: nx.DiGraph):
    plt.rcParams.update({'font.size': 25, 'font.weight': 'bold'})
    nx.draw_circular(graph,
                     with_labels=True,
                     # node_color=color_map,
                     node_size=110)
    plt.show()
#  logic_check_str.check_str import analysis_str
import networkx as nx


def analysis_str(instr: str, graph: nx.DiGraph):
    """ Анализ строки akmc
    """
    current_state = prev_state = 'q0'
    for char in instr:
        print(current_state, f'-{char}->', end=' ')
        for key in graph.adj[current_state].keys():
            prev_state = current_state
            if char == graph.adj[current_state][key]['weigth']:
                current_state = key
                break
        if current_state == prev_state:
            print(f"Invalid str: you can't go anythere from state {current_state} by send {char}")
            return
        if current_state.startswith('f'):
            print("You have arrived at the final state ", current_state)
            return

    print("You have arrived at the state ", current_state)
#  parse.graph_to_file import graph_to_file
import networkx as nx

def write_file(file_name, data: str):
    """ Функция записи данных в файл """
    try:
        f = open(file_name, 'w')
        f.write(data)
        f.close()
    except Exception as e:
        print(e)
    return 1

def graph_to_file(graph: nx.DiGraph, file_name: str):
    data: str = ''
    for begin, end, w in graph.edges.data('weight'):
        data += f'{begin},{w}={end}\n'
    write_file(file_name, data)
    print("The new determined automaton is written to a file:", file_name)
    # print(data)

# from parse.parse_file import parse_file
import re

def read_file(file_name) -> str:
    """ Функция чтения данных(файла) """
    try:
        f = open(file_name, 'r')
        data = f.read()
        f.close()
    except Exception as e:
        print(e)
    return data

def create_graph(transitions: str):
    graph = nx.DiGraph()

    for word in transitions:
        states = re.findall(r'[qf]\d+', word)
        condition = re.findall(r',.=', word)
        condition = condition[0][1:-1]
        graph.add_edge(states[0], states[-1], weight=condition)

    # print(graph.nodes)
    # print(graph.edges)
    return graph

def parse_file(file_name):
    transitions = set(read_file(file_name).split(sep='\n'))
    transitions.remove("")
    transitions = sorted(list(transitions))

    valid = [re.fullmatch(r'q\d+,.=[qf]\d+', s) for s in transitions]
    if None in valid:
        print("Invalid transitions:", transitions[valid.index(None)])
        return None

    return create_graph(transitions)

# from to_deterministic import to_deterministic

import networkx as nx


def to_deterministic(graph: nx.DiGraph):
    """ TODO: ПЕРЕДЕЛАТЬ
    Перевод из недетерминированного автомата в детерминированный

        @:return nx.DiGraph - недетерминированный автомат
    """
    new_graph = nx.DiGraph()
    join_vertex = []
    print(graph.adj)

    print("Joint vertexes: ", end='')
    for key_begin in graph.adj.keys():
        begin = key_begin

        if begin in new_graph.nodes:
            print(new_graph.adj.keys())
            for v in join_vertex:
                if v.find(key_begin) != -1:
                    begin = v

        weigths = {}
        for key_end in graph.adj[key_begin].keys():
            w = graph.adj[key_begin][key_end]['weight']
            # is_not_loop = begin.find(key_end) == -1
            # is_not_loop = True

            if w not in weigths.keys():
                weigths[w] = []
            # if is_not_loop:  # не петля
            weigths[w].append(key_end)

        # print(weigths)
        for key_w in weigths:
            if len(weigths[key_w]) > 1:
                # # Проверяем, что вершина ещё не объединена
                # end = ''
                # for w in weigths[key_w]:
                #     for v in join_vertex:
                #         if v.find(w) == -1:
                #             end += w
                #         else:
                #             end += w[-1]    # добавляем только цифру состояния
                #     if len(join_vertex) == 0:
                end = ''.join(map(str, weigths[key_w]))
                join_vertex.append(end)
                print(end, end=' ')
                new_graph.add_edge(begin, end, weight=key_w)
            else:
                end = weigths[key_w][0]
                # for v in join_vertex:
                #     if v.find(end) != -1:
                #         end = v
                new_graph.add_edge(begin, end, weight=key_w)
    print()
    return new_graph


# from to_deterministic_it import to_deterministic_it
import networkx as nx


def to_deterministic_it(graph: nx.DiGraph):
    """ Перевод из недетерминированного автомата в детерминированный

        @:return nx.DiGraph - недетерминированный автомат
    """
    new_graph = nx.DiGraph()
    join_vertex = []

    print("Joint vertexes: ", end='')
    for key_begin in graph.adj.keys():  # идём по всем вершинам
        begin = key_begin
        weigths = {}
        for key_end in graph.adj[key_begin].keys():
            w = graph.adj[key_begin][key_end]['weight']
            if w not in weigths.keys():
                weigths[w] = []
            weigths[w].append(key_end)

        for key_w in weigths:
            if len(weigths[key_w]) > 1:
                end = ''.join(map(str, weigths[key_w]))
                print(end, end=' ')
                # check внутренние вершины
                for v in weigths[key_w]:
                    for k in join_vertex:   # Проверяем входит ли этот переход в граф
                        if k.find(v) != -1 and new_graph.adj[k][v]['weight'] == key_w:
                            new_graph.remove_edge(k, v)
                            new_graph.remove_node(v)

                    for u in weigths[key_w]:
                        if v != u and (v, u) in graph.edges:
                            new_graph.add_edge(end, u, weight=graph.adj[v][u]['weight'])

                join_vertex.append(end)
            else:
                end = weigths[key_w][0]

            # Проверяем входит ли эта вершина в объединённые
            begin_j = begin
            if begin not in new_graph.nodes:
                for v in join_vertex:
                    if v.find(key_begin) != -1:
                        begin_j = v
                        break
            end_j = end
            if end not in new_graph.nodes:
                for v in join_vertex:
                    if v.find(end) != -1:
                        end_j = v
                        break

            # # Если это не петля
            # if begin != end and begin_j == end_j:
            #     new_graph.add_edge(begin_j, end, weight=key_w)
            # else:
            new_graph.add_edge(begin_j, end_j, weight=key_w)

    print()
    return new_graph




if __name__ == "__main__":
    # file_name = str(input())
    file_name = "test.txt"
    graph = parse_file(file_name)
    if graph is not None:
        # draw(graph)
        if not check_deterministic(graph):
            determ_graph = to_deterministic_it(graph)
            # draw(determ_graph)
            if str(input("Do you want to write determined automate to file? (yes/no)")) == "yes":
                file_name = str(input("Enter a file name "))
                graph_to_file(determ_graph, file_name)
            graph = determ_graph

        if str(input("Do you want to analyze any str? (yes/no)")) == "yes":
            in_str = str(input("Enter a string:\t"))
            analysis_str(in_str, graph)


