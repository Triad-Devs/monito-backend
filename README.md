# Monito

Monito is a user-friendly responsive chat bot in the form of a web app that can be used to monitor application health, security, status, potential issues and other performance metrics over time. The application provides the following features:
- Token based authentication system for secure accession, operation and maintenance of user data
- Application supports monitoring of API endpoints (with JSON payload and authentication header support) and normal website URL’s
- Application monitoring based on the following metrics:
  - Number of requests (Both successful and failed requests)
  - Response time
  - Bytes transferred
  - Network traffic
  - Security statistics, risks and status
- Downloadable audit report for performance, accessibility, Progressive Web Apps (PWA’s) and Search Engine Optimization (SEO)
- Notification and alert system based on alert condition set by user
- Backend API can be integrated with other chat platforms such as slack, discord, telegram, etc

<br/>

**Link to the website:** [https://monito-app.netlify.app](https://monito-app.netlify.app/)
<br/>
**Link to frontend repo:** [https://github.com/Triad-Devs/monito-frontend](https://github.com/Triad-Devs/monito-frontend)
<br/>
**Application demo video link:** [https://youtu.be/mQOaj5VSs1w](https://youtu.be/mQOaj5VSs1w)

<br/>

## Contributors
| Sr. No. | Name     | GitHub |
| ------ | -------- | ----------- |
| 1.     | Viraj Patidar | [@VirajPatidar](https://github.com/VirajPatidar) |
| 2.     | Anurag Singh | [@heyanurag](https://github.com/heyanurag)|
| 3.     | Atharva Patil | [@atharvadpatil](https://github.com/atharvadpatil)|

<br/>

## Architecture
![Architecture](https://github.com/Triad-Devs/monito-backend/blob/main/architecture.png)

<br/>

## Tech Stack
### Backend
- API and Database
  - [Django](https://www.djangoproject.com/)
  - [Django REST Framework](https://www.django-rest-framework.org/)
  - [PostgreSQL](https://www.postgresql.org/)
- Distributed Task Queue and Scheduling
  - [Celery](https://docs.celeryq.dev/en/stable/index.html)
  - [django-celery-beat](https://django-celery-beat.readthedocs.io/en/latest/) 
  - [django-celery-results](https://django-celery-results.readthedocs.io/en/latest/) 
- Message Broker
  - [Redis](https://redis.io/)
- Audit Reports
  - [Lighthouse](https://www.npmjs.com/package/lighthouse)
  - [Express.js](https://expressjs.com/)

### Frontend
- [React](https://reactjs.org/)
- [react-chatbot-kit](https://fredrikoseberg.github.io/react-chatbot-kit-docs/)
- [MUI](https://mui.com/)

<br/>

## Business Impact
- Automatic and intelligent observability will help organizations improve user experiences at the scale of modern computing.
- Business KPIs and user journey analysis (for example, login to check out) to optimize user experiences and provide transparency into how changes impact KPIs
- Root-cause and impact analysis of application performance problems and business outcomes for faster, more reliable incident resolution
- Improved developer and operational productivity
- Improved infrastructure utilization will lead to increase in revenue and reduction in operating cost
- Increased application stability and uptime
- Faster resolution of performance problems and higher-quality software releases

<br/>

## Future Plans and Improvements
- Integration of the developed API with other chat platforms like discord, slack, telegram and WhatsApp
- Support other API formats like GraphQL and gRPC
- Support other authentication types like AWS IAM v4, Oauth, Microsoft NTLM, basic auth and digest.
- Security testing of application for OWASP vulnerabilities using testing platforms like ZAP and Burp Suite
- Refine and extend the notification system to send alerts based on more parameters. Example: Traffic Spike
