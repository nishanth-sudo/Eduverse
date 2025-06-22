# Eduverse: AI-Powered Document Question Answering System

This project is a sophisticated document question-answering system that leverages AI to process PDF documents and provide accurate answers to user queries. The system uses vector embeddings, Firebase for user authentication, and features a modern React frontend with a Flask backend.

## System Architecture

![image](https://github.com/user-attachments/assets/03698918-8c19-40b0-aa91-ac945250443d)

### Architecture Components

1. **Frontend Layer**
   - User Interface: React components for interaction
   - Theme Controller: Manages application theming
   - Auth Controller: Handles user authentication
   - Query Form: Manages user questions and responses

2. **Backend Layer**
   - REST API: Flask-based endpoint handling
   - Request Handler: Processes incoming requests
   - Document Processing Pipeline: Handles document ingestion and processing
   - QA System: Manages context retrieval and answer generation

3. **Storage Layer**
   - Firebase Auth: Handles user authentication
   - PostgreSQL (Neon): Cloud-native PostgreSQL for user history and data
   - Vector Index: FAISS-based vector storage for embeddings
   - Document Cache: Temporary storage for processed documents

### Data Flow

1. **Document Processing Flow**
   - Documents are uploaded through the UI
   - Processing pipeline extracts text and generates embeddings
   - Embeddings are stored in the vector index
   - Document metadata is cached

2. **Query Flow**
   - User submits question through UI
   - Backend retrieves relevant context using vector search
   - Answer generator creates response using context
   - Response is sent back to UI and cached

3. **State Management**
   - User authentication handled by Firebase Auth
   - User history and preferences stored in PostgreSQL (Neon)
   - Authentication state managed in frontend
   - Theme preferences persisted locally

##  Features

- **PDF Document Processing**
  - Automatic text extraction from PDF documents
  - Smart text chunking for improved context understanding
  - Vector embeddings generation for semantic search

- **Advanced Question Answering**
  - Context-aware answer generation
  - Semantic search using FAISS indexing
  - Support for multiple document sources

- **Modern Frontend**
  - React-based user interface with TypeScript
  - Dynamic theme switching (Light/Dark/System)
  - Responsive design with Tailwind CSS
  - Smooth animations with Framer Motion

- **Robust Backend**
  - Flask REST API
  - Firebase integration for data persistence
  - Efficient vector search implementation
  - Modular architecture for easy extensibility

## Project Structure

```
├── app.py                 # Flask application entry point
├── config.py             # Configuration settings
├── database.py           # Database models and setup
├── firebase_db.py        # Firebase integration
├── processor.py          # Document processing logic
├── requirements.txt      # Python dependencies
│
├── frontend/            # React frontend application
│   ├── src/
│   ├── package.json
│   └── ...
│
├── embeddings/          # Vector embedding utilities
├── generation/          # Answer generation logic
├── retrieval/           # Document retrieval system
├── utils/              # Utility functions
└── tests/              # Test suite
```

##  Key Features Implementation

### Document Processing
The system processes documents through several stages:
1. PDF text extraction
2. Text chunking for context preservation
3. Vector embedding generation
4. FAISS index creation for efficient search

### Answer Generation
1. Query vector generation
2. Semantic search for relevant contexts
3. Context-aware answer generation
4. Response formatting and delivery

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request


##  Future Improvements

- [ ] Add support for more document formats
- [ ] Implement real-time collaborative features
- [ ] Add document summarization
- [ ] Enhance answer accuracy with multiple model consensus
- [ ] Implement caching for improved performance
- [ ] Add support for document annotation
- [ ] Implement user feedback system

##  Support

For support, email [mishanthp03032005@gmail.com](nishanthp03032005@gmail.com) or open an issue in the repository.
