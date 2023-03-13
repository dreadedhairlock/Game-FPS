from collections import deque

class CariJalan:
    def __init__(self, game):
        self.game = game
        self.peta = game.peta.minimap
        self.jalan = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graf = {}
        self.get_graf()
    
    def get_path(self, start, goal):
        self.dikunjungi = self.bfs(start, goal, self.graf)
        path = [goal]
        step = self.dikunjungi.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.dikunjungi[step]
        return path [-1]

    def bfs(self, start, goal, graf):
        queue = deque([start])
        dikunjungi = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graf[cur_node]

            for next_node in next_nodes:
                if next_node not in dikunjungi and next_node not in self.game.objecthandler.npc_position:
                    queue.append(next_node)
                    dikunjungi[next_node] = cur_node
        return dikunjungi

    def get_next_node(self, x, y):
        return[(x + dx, y + dy) for dx, dy in self.jalan if (x + dx, y + dy) not in self.game.peta.peta_dunia]

    def get_graf(self):
        for y, row in enumerate(self.peta):
            for x, col in enumerate(row):
                if not col:
                    self.graf[(x, y)] = self.graf.get((x, y), []) + self.get_next_node(x, y)
