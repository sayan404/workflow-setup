# Backend - Pipeline Validation API

A FastAPI-based backend service that provides pipeline validation, analysis, and processing capabilities for the visual workflow builder. The backend validates pipeline structures, checks for Directed Acyclic Graphs (DAGs), and provides comprehensive error handling.

## 🎯 Overview

The backend service provides:
- **Pipeline Validation**: Ensures workflows are properly structured
- **DAG Detection**: Validates that pipelines form valid Directed Acyclic Graphs
- **RESTful API**: Clean, documented API endpoints
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Error Handling**: Comprehensive error responses and logging

## 🏗️ Project Structure

```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Python-dotenv** - Environment variable management
- **Uvicorn** - ASGI server for running FastAPI applications
- **Python 3.8+** - Modern Python with type hints

## 📦 Dependencies

### Core Dependencies
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server implementation
- `pydantic` - Data validation and settings management
- `python-dotenv` - Environment variable loading
- `typing` - Type hints support

### Optional Dependencies
- `pytest` - Testing framework
- `httpx` - HTTP client for testing
- `black` - Code formatting
- `flake8` - Linting

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   # Create .env file
   echo "FRONTEND_URL=http://localhost:3000" > .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Development Settings
DEBUG=True
LOG_LEVEL=INFO
```

### CORS Configuration

The application is configured with CORS middleware to allow frontend communication:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

## 📚 API Documentation

### Endpoints

#### `POST /pipelines/parse`

Validates and analyzes pipeline structure.

**Request Body:**
```json
{
  "nodes": [
    {
      "id": "node-1",
      "type": "customInput",
      "position": {"x": 100, "y": 100},
      "data": {"id": "node-1", "nodeType": "customInput"}
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "target": "node-2"
    }
  ]
}
```

**Response:**
```json
{
  "num_nodes": 2,
  "num_edges": 1,
  "is_dag": true
}
```

**Error Response:**
```json
{
  "detail": "Error processing pipeline: [error message]"
}
```

### Data Models

#### PipelineData
```python
class PipelineData(BaseModel):
    nodes: List[dict]
    edges: List[dict]
```

## 🔍 Pipeline Validation Logic

### DAG Detection Algorithm

The backend uses a topological sort algorithm to validate that the pipeline forms a valid Directed Acyclic Graph:

1. **Build Adjacency List**: Create a graph representation from edges
2. **Calculate Indegrees**: Count incoming edges for each node
3. **Topological Sort**: Process nodes with zero indegree
4. **Validation**: Check if all nodes are reachable (no cycles)

### Algorithm Implementation

```python
def validate_dag(nodes, edges):
    # Build graph and calculate indegrees
    graph = defaultdict(list)
    indegree = defaultdict(int)
    
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        graph[source].append(target)
        indegree[target] += 1
        if source not in indegree:
            indegree[source] = 0
    
    # Topological sort
    zero_indegree_queue = deque([node for node in indegree if indegree[node] == 0])
    visited_count = 0
    
    while zero_indegree_queue:
        current = zero_indegree_queue.popleft()
        visited_count += 1
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_indegree_queue.append(neighbor)
    
    return visited_count == len(nodes)
```

## 🧪 Testing

### Running Tests

1. **Install test dependencies**
   ```bash
   pip install pytest httpx
   ```

2. **Run tests**
   ```bash
   pytest
   ```

3. **Run with coverage**
   ```bash
   pip install pytest-cov
   pytest --cov=main
   ```

### Test Examples

```python
def test_pipeline_validation():
    # Test valid DAG
    pipeline_data = {
        "nodes": [{"id": "1"}, {"id": "2"}],
        "edges": [{"source": "1", "target": "2"}]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    assert response.json()["is_dag"] == True

def test_invalid_pipeline():
    # Test cyclic graph
    pipeline_data = {
        "nodes": [{"id": "1"}, {"id": "2"}],
        "edges": [
            {"source": "1", "target": "2"},
            {"source": "2", "target": "1"}
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    assert response.json()["is_dag"] == False
```

## 🚀 Deployment

### Development Server

```bash
python main.py
```

### Production Server

Using Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Using Gunicorn:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t workflow-backend .
docker run -p 8000:8000 workflow-backend
```

## 🔒 Security Considerations

### CORS Configuration
- Configure allowed origins properly
- Use environment variables for sensitive settings
- Implement proper authentication if needed

### Input Validation
- All inputs are validated using Pydantic models
- Type checking and data validation
- Error handling for malformed requests

### Error Handling
- Comprehensive exception handling
- Detailed error messages for debugging
- Proper HTTP status codes

## 📊 Performance

### Optimization Strategies
- **Efficient Algorithms**: O(V + E) time complexity for DAG validation
- **Memory Management**: Minimal memory footprint
- **Async Support**: FastAPI's async capabilities for high concurrency

### Monitoring
- Request/response logging
- Performance metrics
- Error tracking

## 🔧 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes

### Linting and Formatting
```bash
# Install development tools
pip install black flake8

# Format code
black main.py

# Lint code
flake8 main.py
```

### Adding New Endpoints

1. **Define the endpoint**
   ```python
   @app.post('/new-endpoint')
   def new_endpoint(data: NewDataModel):
       # Implementation
       return {"result": "success"}
   ```

2. **Add data models**
   ```python
   class NewDataModel(BaseModel):
       field1: str
       field2: int
   ```

3. **Add tests**
   ```python
   def test_new_endpoint():
       # Test implementation
       pass
   ```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check FRONTEND_URL environment variable
   - Verify frontend is running on correct port
   - Check browser console for CORS errors

2. **Import Errors**
   - Ensure virtual environment is activated
   - Check all dependencies are installed
   - Verify Python version compatibility

3. **Port Already in Use**
   - Change port in environment variables
   - Kill existing processes on the port
   - Use different port for development

### Debug Mode

Enable debug mode by setting:
```python
# In main.py
app = FastAPI(debug=True)
```

## 🔮 Future Enhancements

- **Authentication and Authorization**
- **Database Integration**
- **Pipeline Execution Engine**
- **Real-time WebSocket Support**
- **Advanced Validation Rules**
- **Performance Monitoring**
- **API Rate Limiting**
- **Caching Layer**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure code passes linting
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review error logs
3. Open an issue in the repository
4. Check FastAPI documentation for general questions 