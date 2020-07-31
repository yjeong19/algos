import collections
from enum import Enum

class FlowVertex:
    Infinity = float("inf")

    class EmptySortTypeStack(Exception):
        pass

    class SortType(Enum):
        DIST = 0
        DATA = 1

    sort_key = [SortType.DATA]

    def __init__(self, data=None):
        self.data = data
        self.edge_pairs = dict()
        # just the flow, gets the flow from res graph
        self.flow_pairs = dict()
        # res graph has a reverse flow starts with 0
        self.res_pairs = dict()

        self.dist = None
        self.prev_in_path = None

    def add_adj(self, vertex, cost=None):
        # temp leaving edige_pairs to compare
        self.edge_pairs[vertex] = cost
        self.res_pairs[vertex] = [cost, 0]
        self.flow_pairs[vertex] = 0

    @classmethod
    def push_sort_type(cls, sort_type):
        cls.sort_key.append(sort_type)

    @classmethod
    def pop_sort_type(cls):
        if len(cls.sort_key) > 1:
            cls.sort_key.pop()
        else:
            raise FlowVertex.EmptySortTypeStack

    def __lt__(self, other):
        if self.sort_key[-1] is self.SortType.DIST:
            return self.dist < other.dist
        elif self.sort_key[-1] is self.SortType.DATA:
            return self.data < other.data

    def __eq__(self, other):
        if self.sort_key[-1] is self.SortType.DIST:
            return self.dist == other.dist
        elif self.sort_key[-1] is self.SortType.DATA:
            return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def show_adj_res_list(self):
        print("Adj list for ", self.data, ": ", sep="", end="")
        for vertex in self.edge_pairs:
            print(vertex.data, "(", self.res_pairs[vertex], ")",
                  sep="", end=" ")

    def show_adj_flow_list(self):
        print("Adj list for ", self.data, ": ", sep="", end="")
        for vertex in self.edge_pairs:
            print(vertex.data, "(", self.flow_pairs[vertex], ")",
                  sep="", end=" ")


class Max_Flow_Graph:
    def __init__(self):
        self._vertices = dict()
        self.start = None
        self.end = None

    def add_edge(self, src, dest, cost=None):
        # res_pairs will receive two edges based on this one call:
        # a forward edge, exactly as before and a reverse edge with cost 0

        # flow_pairs is built as before but with all costs = 0
        src_vertex = self.get_vertex_object(src)
        dest_vertex = self.get_vertex_object(dest)
        src_vertex.add_adj(dest_vertex, cost)

    def find_max_flow(self):
        """
            The method loops, calling establish_next_flow_path() followed by get_limiting_flow_on_res_path()
            and follows those calls by adjusting the residual and flow graphs using adjust_path_by_cost().
            When establish_next_flow_path() returns false (or adjust_path_by_cost() returns false or the
            limiting flow becomes 0, take your pick), the loop ends. Finally, the flow graph is probed to
            find the total flow for the functional return.
        """
        next_flow = self.establish_next_flow_path()

        while next_flow:
            cost = self.get_limiting_flow_on_res_path()
            self.adjust_path_by_cost(cost)
            self.show_res_adj_table()
            self.show_flow_adj_table()
            next_flow = self.establish_next_flow_path()

        max_flow = 0
        for vcost in self._vertices[self.start].flow_pairs.values():
            max_flow += vcost

        return max_flow


    def establish_next_flow_path(self):
        """
            this is based on the dijkstra() method.  It is less demanding than dijkstra because any path that connects
            _start to _end will do.  The simplest way to convert dijkstra to this method is:
            Remove the functional parameter, since we will always start at the vertex start.
            When traversing a newly popped v's adjacency lists, skip edges with cost == 0 since they have been
            reduced to nothing (and are effectively no longer in the residual graph).
            End the loop as soon as it finds a path to end.  We don't care about finding other flow paths since,
            in this version, it will be looking for "shorter" paths, something that is not necessarily good for us here.
            It returns true if end was successfully reached and false, otherwise.
        """
        Infinity = float('inf')
        src_vertex = self._vertices[self.start]
        partially_processed = collections.deque()

        for vdata, vobj in self._vertices.items():
            vobj.dist = Infinity
        src_vertex.dist = 0
        partially_processed.append(src_vertex)
        current_src = self.start

        while current_src != self.end:
            current_vertex = partially_processed.popleft()
            current_src = current_vertex.data
            for vobj in current_vertex.res_pairs:
                if current_vertex.dist + current_vertex.res_pairs[vobj][0] < vobj.dist \
                        and current_vertex.res_pairs[vobj][0] != 0:
                    vobj.dist = current_vertex.dist + current_vertex.res_pairs[vobj][0]
                    partially_processed.append(vobj)
                    vobj.prev_in_path = current_vertex
                # this reverse causes infinit loop
                # elif current_vertex.dist + current_vertex.res_pairs[vobj][1] < vobj.dist \
                #         and current_vertex.res_pairs[vobj][1] != 0:
                #     vobj.dist = current_vertex.dist + current_vertex.res_pairs[vobj][0]
                #     partially_processed.append(vobj)
                #     vobj.prev_in_path = current_vertex

            if len(partially_processed) == 0 and current_src != self.end:
                return False

        return True

    def get_limiting_flow_on_res_path(self):
        """
             a helper for find_max_flow() which follows on the coattails of establish_next_flow_path() and uses the data
             and path just created to find the limiting flow (minimum) of the residual path just found.
             The method show_shortest_path() (which we don't need for this class) demonstrates how to trace the path
             from end to start, a maneuver that is useful here.
        """
        limiting_flow = float('inf')
        source = self._vertices[self.start]
        sink = self._vertices[self.end]
        self.establish_next_flow_path()

        if sink.dist < float('inf'):
            current_vert = sink
            while current_vert is not source:
                current_flow = current_vert.prev_in_path.res_pairs[current_vert][0]
                limiting_flow = min(limiting_flow, current_flow)
                current_vert = current_vert.prev_in_path
        return limiting_flow

    def adjust_path_by_cost(self, cost):
        """
         a helper for find_max_flow() which takes the result of  get_limiting_flow_on_res_path() and uses it to modify
         the costs of edges in both the residual graph and the flow graph.  Again, chasing the path from end-to-start
         will be the dominant action here.  Because the path was based on an ad-hoc linked list using prev_in_path,
         from end-to-start, the two vertices in each loop pass (say, current_vert and current_vert->prev_in_path)
         must be used to access the correct cost on the correct adjacency list.  That's the job of the next two methods:
        """
        source = self._vertices[self.start]
        sink = self._vertices[self.end]

        current_vert = sink
        while current_vert != source:
            # subtract from resdial flow
            self.add_cost_to_res_edge(current_vert, current_vert.prev_in_path, cost)
            self.add_cost_to_flow_edge(current_vert, current_vert.prev_in_path, cost)
            current_vert = current_vert.prev_in_path

        # checking path
        test_curr = self._vertices[self.end]
        while test_curr.data != self.start:
            test_curr = self._vertices[test_curr.data].prev_in_path

    def add_cost_to_res_edge(self, src, dst, cost):
        """
         a helper to adjust_path_by_cost(), this method examines src's residual adjacency list to find dst and
         then add cost to that edge (cost can be negative if adjust_path_by_cost() wants to subtract rather than add).
        """
        dst.res_pairs[src][0] -= cost
        # add to reverse flow
        dst.res_pairs[src][1] += cost

    def add_cost_to_flow_edge(self, src, dst, cost):
        """
             a helper to adjust_path_by_cost(), this method examines src's flow adjacency list to find dst and then
             adds cost to that edge.  If dst is not found in src's list, that implies that the edge passed in was
             actually a reverse edge, in which case the flow edge we need to adjust is (dst, src).
             Further, this means we need to subtract the flow because residual flow in the reverse direction is a
             signal that we are undoing some flow previously added.
        """
        try:
            dst.flow_pairs[src] += cost
        except KeyError:
            src.flow_pairs[dst] -= cost

    def show_res_adj_table(self):
        print('\n----- Res Table -------')
        for v in self._vertices:
            self._vertices[v].show_adj_res_list()
            print("\n")

    def show_flow_adj_table(self):
        print('\n----- Flow Table -----')
        for v in self._vertices:
            self._vertices[v].show_adj_flow_list()
            print("\n")

    def get_vertex_object(self, vertex_data):
        try:
            vertex = self._vertices[vertex_data]
            return vertex
        except KeyError:
            FlowVertex.push_sort_type(FlowVertex.SortType.DATA)
            new_vertex = FlowVertex(vertex_data)
            self._vertices[vertex_data] = new_vertex
            FlowVertex.pop_sort_type()
            return new_vertex

    def clear(self):
        self._vertices = {}


def main():
    graph = Max_Flow_Graph()
    graph.add_edge("s", "a", 3)
    graph.add_edge("s", "b", 2)
    graph.add_edge("a", "b", 1)
    graph.add_edge("a", "c", 3)
    graph.add_edge("a", "d", 4)
    graph.add_edge("b", "d", 2)
    graph.add_edge("c", "t", 2)
    graph.add_edge("d", "t", 3)

    graph.show_res_adj_table()
    graph.show_flow_adj_table()

    graph.start = "s"
    graph.end = "t"

    final_flow = graph.find_max_flow()

    print(f"Final flow: {final_flow}")

    graph.show_res_adj_table()
    graph.show_flow_adj_table()


if __name__ == "__main__":
    main()

"""

----- Res Table -------
Adj list for s: a([3, 0]) b([2, 0]) 

Adj list for a: b([1, 0]) c([3, 0]) d([4, 0]) 

Adj list for b: d([2, 0]) 

Adj list for c: t([2, 0]) 

Adj list for d: t([3, 0]) 

Adj list for t: 


----- Flow Table -----
Adj list for s: a(0) b(0) 

Adj list for a: b(0) c(0) d(0) 

Adj list for b: d(0) 

Adj list for c: t(0) 

Adj list for d: t(0) 

Adj list for t: 


----- Res Table -------
Adj list for s: a([3, 0]) b([0, 2]) 

Adj list for a: b([1, 0]) c([3, 0]) d([4, 0]) 

Adj list for b: d([0, 2]) 

Adj list for c: t([2, 0]) 

Adj list for d: t([1, 2]) 

Adj list for t: 


----- Flow Table -----
Adj list for s: a(0) b(2) 

Adj list for a: b(0) c(0) d(0) 

Adj list for b: d(2) 

Adj list for c: t(0) 

Adj list for d: t(2) 

Adj list for t: 


----- Res Table -------
Adj list for s: a([1, 2]) b([0, 2]) 

Adj list for a: b([1, 0]) c([1, 2]) d([4, 0]) 

Adj list for b: d([0, 2]) 

Adj list for c: t([0, 2]) 

Adj list for d: t([1, 2]) 

Adj list for t: 


----- Flow Table -----
Adj list for s: a(2) b(2) 

Adj list for a: b(0) c(2) d(0) 

Adj list for b: d(2) 

Adj list for c: t(2) 

Adj list for d: t(2) 

Adj list for t: 


----- Res Table -------
Adj list for s: a([0, 3]) b([0, 2]) 

Adj list for a: b([1, 0]) c([1, 2]) d([3, 1]) 

Adj list for b: d([0, 2]) 

Adj list for c: t([0, 2]) 

Adj list for d: t([0, 3]) 

Adj list for t: 


----- Flow Table -----
Adj list for s: a(3) b(2) 

Adj list for a: b(0) c(2) d(1) 

Adj list for b: d(2) 

Adj list for c: t(2) 

Adj list for d: t(3) 

Adj list for t: 

Final flow: 5

----- Res Table -------
Adj list for s: a([0, 3]) b([0, 2]) 

Adj list for a: b([1, 0]) c([1, 2]) d([3, 1]) 

Adj list for b: d([0, 2]) 

Adj list for c: t([0, 2]) 

Adj list for d: t([0, 3]) 

Adj list for t: 


----- Flow Table -----
Adj list for s: a(3) b(2) 

Adj list for a: b(0) c(2) d(1) 

Adj list for b: d(2) 

Adj list for c: t(2) 

Adj list for d: t(3) 

Adj list for t: 
"""