# Technology Stack

This document defines the technology stack for Everyday Rhythm project. Other documentation files reference this as the single source of truth.

## Frontend Technologies

### Framework
- **Primary**: Pygame
- **Version**: 2.5.0 or higher
- **Rationale**: Cross-platform game development library with excellent audio support

### Language
- **Primary**: Python
- **Version**: 3.10+
- **Configuration**: Type hints enabled, modern Python features

### Audio Processing
- **Framework**: pydub for audio manipulation
- **Analysis**: librosa for music analysis
- **Formats**: .mp3, .wav support

## Backend Technologies

### Runtime Environment
- **Platform**: Python
- **Version**: 3.10+ 
- **Rationale**: Excellent library ecosystem for audio processing and AI integration

### AI Integration
- **Primary**: Amazon Q Developer API
- **Purpose**: Natural language to stage generation
- **Authentication**: API key management

### Data Format
- **Stage Data**: JSON format
- **Audio Files**: .mp3, .wav formats
- **Configuration**: Python dictionaries and JSON

## Database Technologies

### Primary Storage
- **Type**: Local JSON files
- **Purpose**: Stage templates and configuration
- **Format**: Structured JSON with stage metadata

### Audio Storage
- **Location**: Local filesystem
- **Organization**: assets/ directory structure
- **Formats**: .mp3, .wav files

## Infrastructure

### Platform
- **Primary**: Local development (macOS)
- **Rationale**: Simple deployment, privacy protection, no server management

### Development Environment
- **OS**: macOS Sonoma (14.x) or higher
- **Python**: Virtual environment management
- **Dependencies**: pip and requirements.txt

### AI Services
- **Stage Generation**: Amazon Q Developer API
- **Usage**: On-demand stage creation from natural language

## DevOps & CI/CD

### Version Control
- **Platform**: GitHub
- **Workflow**: GitHub Flow with feature branches
- **Strategy**: Trunk-based development with short-lived feature branches

### CI/CD Pipeline
- **Platform**: GitHub Actions
- **Deployment**: Blue-Green deployment using AWS CDK
- **Environments**: Development → Staging → Production

### Monitoring & Observability
- **Application Monitoring**: AWS CloudWatch + AWS X-Ray
- **Infrastructure Monitoring**: AWS CloudWatch
- **Logging**: AWS CloudWatch Logs with structured logging
- **Tracing**: AWS X-Ray for distributed tracing

## Development Tools

### Code Quality
- **Linting**: ESLint with TypeScript rules
- **Formatting**: Prettier with consistent configuration
- **Type Checking**: TypeScript strict mode

### Testing
- **Unit Testing**: Jest with TypeScript support
- **Integration Testing**: Jest with AWS SDK mocks
- **E2E Testing**: Playwright for browser automation
- **Performance Testing**: Artillery for load testing

### Documentation
- **API Docs**: OpenAPI/Swagger generated documentation
- **Code Docs**: TSDoc for TypeScript documentation
- **Project Docs**: Markdown files in docs/ directory

## Security

### Authentication
- **Method**: JWT tokens
- **Provider**: AWS Cognito User Pools
- **Features**: Multi-factor authentication, password policies, account recovery

### Authorization
- **Pattern**: Role-Based Access Control (RBAC)
- **Implementation**: AWS Cognito Groups + IAM roles

### Data Protection
- **Encryption**: AES-256 for data at rest, TLS 1.3 for data in transit
- **Secrets Management**: AWS Secrets Manager for API keys and sensitive configuration

## External Services

### Communication
- **Email**: Amazon SES for transactional emails
- **Push Notifications**: AWS SNS for mobile notifications (future)

### File Storage
- **Service**: Amazon S3 for game assets and user uploads
- **CDN**: Amazon CloudFront for global content delivery

### Analytics
- **Web Analytics**: AWS CloudWatch Insights for custom analytics
- **Error Tracking**: AWS CloudWatch Logs + custom error aggregation

### Payment Processing
- **Provider**: Not applicable for MVP (future consideration: Stripe)

## Version Requirements

| Technology | Minimum Version | Recommended Version | Notes |
|------------|----------------|-------------------|-------|
| Node.js | 18.0.0 | 18.17.0 | AWS Lambda runtime |
| TypeScript | 5.0.0 | 5.1.6 | Latest stable |
| React | 18.0.0 | 18.2.0 | Concurrent features |
| Vite | 4.0.0 | 4.4.0 | Latest stable |
| AWS CDK | 2.80.0 | 2.90.0+ | Latest stable |

## Decision Rationale

### Why These Technologies?

1. **Serverless Architecture**: Eliminates server management, provides automatic scaling, and offers pay-per-use pricing model perfect for gaming workloads with variable traffic.

2. **AWS Ecosystem**: Comprehensive set of managed services specifically designed for gaming applications, including real-time communication, user management, and global content delivery.

3. **TypeScript Everywhere**: Type safety across the entire stack reduces bugs, improves developer experience, and enables better refactoring capabilities.

4. **React + Vite**: Modern frontend development with fast development server, optimized builds, and excellent developer experience.

### Alternative Considerations

| Technology | Alternative Considered | Why Not Chosen |
|------------|----------------------|----------------|
| AWS Lambda | Express.js on EC2 | Serverless provides better scaling and cost efficiency |
| DynamoDB | PostgreSQL on RDS | NoSQL better suited for gaming data patterns and scaling |
| React | Vue.js/Angular | React has larger ecosystem and better AWS integration |
| Tailwind CSS | Styled Components | Utility-first approach provides better consistency |

## Migration Path

### Current → Target
Starting from scratch, no migration needed.

### Future Enhancements
1. **Phase 1**: Add ElastiCache for improved performance
2. **Phase 2**: Implement AWS GameLift for advanced matchmaking
3. **Phase 3**: Add mobile app with React Native

## Dependencies

### Critical Dependencies
- **AWS SDK v3**: Core AWS service integration
- **React**: Frontend framework
- **TypeScript**: Type safety and developer experience
- **AWS CDK**: Infrastructure management

### Optional Dependencies
- **Zustand**: State management (could use React Context as fallback)
- **React Query**: Server state management (could use custom hooks)
- **Tailwind CSS**: Styling (could use CSS modules as fallback)

---

**Last Updated**: 2025-06-15  
**Reviewed By**: Amazon Q Game Challenge Team  
**Next Review**: 2025-07-15
