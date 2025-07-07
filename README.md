# Workflow Setup - Visual Pipeline Builder

A modern web application for creating and validating visual workflows/pipelines with drag-and-drop functionality. This project consists of a React frontend for the visual interface and a FastAPI backend for pipeline validation and processing.

## 🚀 Features

- **Visual Pipeline Builder**: Drag-and-drop interface for creating workflows
- **Multiple Node Types**: Input, Output, LLM, Text, and Calculation nodes
- **Real-time Validation**: Backend validation of pipeline structure (DAG checking)
- **Modern UI**: Built with React and ReactFlow for smooth user experience
- **RESTful API**: FastAPI backend with comprehensive error handling

## 🏗️ Architecture

```
workflow-setup/
├── frontend/          # React application with ReactFlow
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── nodes/         # Custom node implementations
│   │   ├── store.js       # State management (Zustand)
│   │   └── ...
│   └── package.json
├── backend/           # FastAPI application
│   ├── main.py        # Main API server
│   └── requirements.txt
└── README.md          # This file
```

## 🛠️ Technology Stack

### Frontend

- **React 18.2.0** - UI framework
- **ReactFlow 11.8.3** - Visual workflow builder
- **Zustand** - State management
- **React Scripts** - Build and development tools

### Backend

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Python-dotenv** - Environment variable management
- **CORS** - Cross-origin resource sharing

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn** package manager

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd workflow-setup
```

### 2. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 3. Set Up Frontend

```bash
cd frontend
npm install
npm start
```

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 📖 Detailed Setup

See individual README files for detailed setup instructions:

- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
FRONTEND_URL=http://localhost:3000
```

## 📚 API Documentation

The backend provides the following endpoints:

- `POST /pipelines/parse` - Validate and analyze pipeline structure

### Pipeline Data Format

```json
{
  "nodes": [
    {
      "id": "node-1",
      "type": "customInput",
      "position": { "x": 100, "y": 100 },
      "data": { "id": "node-1", "nodeType": "customInput" }
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

## 🧪 Testing

### Frontend Testing

```bash
cd frontend
npm test
```

### Backend Testing

```bash
cd backend
# Add your testing commands here
```

## 📦 Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

### Backend Deployment

The FastAPI application can be deployed using:

- **Uvicorn**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Gunicorn**: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the individual README files for specific component documentation
2. Review the API documentation at http://localhost:8000/docs (when backend is running)
3. Open an issue in the repository

## 🔄 Development Workflow

1. **Frontend Development**: Work in the `frontend/` directory
2. **Backend Development**: Work in the `backend/` directory
3. **API Testing**: Use the FastAPI automatic documentation at `/docs`
4. **State Management**: Frontend uses Zustand for global state management

## 🎯 Project Goals

- Provide an intuitive visual interface for workflow creation
- Ensure pipeline validation and error handling
- Support multiple node types for different operations
- Maintain clean separation between frontend and backend
- Enable easy extension and customization
