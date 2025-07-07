# /backend/main.
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from collections import defaultdict, deque
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = FastAPI()
# Added CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL" )],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"]
)

# Define the input schema
class PipelineData(BaseModel):
    nodes: List[dict]
    edges: List[dict]

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineData):
    try:
        # Count nodes and edges
        num_nodes = len(pipeline.nodes)
        num_edges = len(pipeline.edges)

        # Build adjacency list to check for DAG
        graph = defaultdict(list)
        indegree = defaultdict(int)

        for edge in pipeline.edges:
            source = edge["source"]
            target = edge["target"]
            graph[source].append(target)
            indegree[target] += 1
            if source not in indegree:
                indegree[source] = 0

        # Topological Sort to check if it's a DAG
        zero_indegree_queue = deque([node for node in indegree if indegree[node] == 0])
        visited_count = 0

        while zero_indegree_queue:
            current = zero_indegree_queue.popleft()
            visited_count += 1
            for neighbor in graph[current]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    zero_indegree_queue.append(neighbor)

        is_dag = visited_count == num_nodes

        return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing pipeline: {str(e)}")
