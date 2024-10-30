import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import heapq
import cv2

@dataclass
class Connection:
    start: int
    end: int
    is_indoor: bool
    stairs: int  # positive for up, negative for down
    road_crossings: int


class PathFinder:
    def __init__(self, positions: np.ndarray, connections: List[Connection]):
        """
        Initialize the PathFinder with positions and connections

        Args:
            positions: numpy array of shape (n, 2) containing x,y coordinates
            connections: list of Connection objects defining the graph edges
        """
        self.positions = positions
        self.connections = connections
        self.num_vertices = len(positions)
        self.graph = self._build_graph()
        self.road_crossing_weight = 4.0
        self.rain_weight = 3.0
        self.sunny_weight = 2.0
        self.stair_weight = 0.5 # per step

    def _calculate_distance(self, point1: np.ndarray, point2: np.ndarray) -> float:
        """Calculate Euclidean distance between two points"""
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def _build_graph(self) -> Dict[int, List[Tuple[int, Connection]]]:
        """
        Build adjacency list representation of the graph
        """
        graph = {i: [] for i in range(self.num_vertices)}

        for conn in self.connections:
            # Add connection in both directions (undirected graph)
            graph[conn.start].append((conn.end, conn))
            graph[conn.end].append((conn.start, conn))

        return graph

    def _calculate_cost(self, connection: Connection, rain_prob: float, uv_index: float) -> float:
        """
        Calculate the cost of using a connection based on various factors
        """
        # Calculate base cost from Euclidean distance
        base_cost = self._calculate_distance(
            self.positions[connection.start],
            self.positions[connection.end]
        )

        # Weather effects for outdoor paths
        if not connection.is_indoor:
            weather_factor = (rain_prob * self.rain_weight) + (uv_index * self.sunny_weight)
            base_cost *= (1.0 + weather_factor)

        # Stairs penalty (only for going up)
        if connection.stairs > 0:
            base_cost += connection.stairs * self.stair_weight

        # Road crossing penalty
        base_cost += connection.road_crossings * self.road_crossing_weight

        return base_cost

    def find_shortest_path(self, start: int, end: int, rain_prob: float = 0.0,
                           uv_index: float = 0.0) -> Tuple[List[int], float]:
        """
        Find the optimal path using Dijkstra's algorithm with custom weights

        Args:
            start: starting vertex index
            end: ending vertex index
            rain_prob: probability of rain (0.0-1.0)
            uv_index: UV index (0.0-1.0)

        Returns:
            tuple of (path as list of vertices, total cost)
        """
        # Initialize distances and predecessors
        distances = {v: float('infinity') for v in range(self.num_vertices)}
        distances[start] = 0
        predecessors = {v: None for v in range(self.num_vertices)}

        # Priority queue for Dijkstra's algorithm
        pq = [(0, start)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            # If we've reached the destination
            if current_vertex == end:
                break

            # If we've found a worse path
            if current_distance > distances[current_vertex]:
                continue

            # Check all neighbors
            for neighbor, connection in self.graph[current_vertex]:
                cost = self._calculate_cost(connection, rain_prob, uv_index)
                distance = current_distance + cost

                # If we've found a better path
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return path, distances[end]

    def visualize(self, map_image: np.ndarray, highlighted_path: Optional[List[int]] = None) -> np.ndarray:
        """
        Create a visualization of the graph overlaid on a map image

        Args:
            map_image: numpy array of shape (H, W, 3) containing the background map
            highlighted_path: optional list of vertex indices representing a path to highlight

        Returns:
            numpy array of shape (H, W, 3) containing the visualization
        """
        # Create a copy of the map image
        vis_image = map_image.copy()

        # Define colors (BGR format)
        INDOOR_COLOR = (0, 200, 0)  # Green
        OUTDOOR_COLOR = (203, 192, 255)  # Pink
        ROAD_COLOR = (0, 0, 0)  # Black
        POINT_COLOR = (0, 0, 255)  # Red
        PATH_COLOR = (255, 165, 0)  # Blue

        # Draw connections
        for conn in self.connections:
            start_pos = tuple(map(int, self.positions[conn.start]))
            end_pos = tuple(map(int, self.positions[conn.end]))

            # Choose base color based on indoor/outdoor status
            color = INDOOR_COLOR if conn.is_indoor else OUTDOOR_COLOR

            # Draw road crossing if present
            if conn.road_crossings > 0: color = ROAD_COLOR

            # Draw the main connection line
            if conn.stairs != 0:
                # Create dashed line for stairs
                dash_length = 5
                direction = np.array(end_pos) - np.array(start_pos)
                length = np.linalg.norm(direction)
                direction = direction / length

                num_dashes = int(length / (2 * dash_length))
                for i in range(num_dashes):
                    dash_start = np.array(start_pos) + (2 * i * dash_length) * direction
                    dash_end = dash_start + dash_length * direction
                    cv2.line(vis_image,
                             tuple(map(int, dash_start)),
                             tuple(map(int, dash_end)),
                             color, 2)
            else:
                cv2.line(vis_image, start_pos, end_pos, color, 2)

        # Draw positions (points)
        for pos in self.positions:
            pos_tuple = tuple(map(int, pos))
            cv2.circle(vis_image, pos_tuple, 5, POINT_COLOR, -1)
            cv2.circle(vis_image, pos_tuple, 7, (0, 0, 0), 1)

        # Draw highlighted path if provided
        if highlighted_path and len(highlighted_path) > 1:
            for i in range(len(highlighted_path) - 1):
                start_pos = tuple(map(int, self.positions[highlighted_path[i]]))
                end_pos = tuple(map(int, self.positions[highlighted_path[i + 1]]))
                cv2.line(vis_image, start_pos, end_pos, PATH_COLOR, 4)

        return vis_image

def main():
    map_image = cv2.imread("NTU_minimap.png")

    from map import positions, connections
    finder = PathFinder(positions, connections)

    vis_map = finder.visualize(map_image)
    cv2.imshow(f"Path Visualization", vis_map)

    # Test different weather conditions
    # (Rain probability, UV index, weather name)
    weather_conditions = [
        (0.0, 0.0, "Clear weather"),
        (0.8, 0.2, "Rainy weather"),
        (0.0, 0.9, "Sunny weather")
    ]

    for rain_prob, uv_index, condition in weather_conditions:
        # Find optimal path
        path, cost = finder.find_shortest_path(0, 22, rain_prob, uv_index)
        print(f"\nCondition: {condition}")
        print(f"Optimal path: {' -> '.join(map(str, path))}")
        print(f"Total cost: {cost:.2f}")

        # Create visualization with highlighted path
        vis_search = finder.visualize(map_image, highlighted_path=path)

        # Add text for weather condition
        cv2.putText(vis_search, condition, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        # Display the image
        cv2.imshow(f"Path Visualization - {condition}", vis_search)
        cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()