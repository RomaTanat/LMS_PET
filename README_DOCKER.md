# LMS Project - Docker Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- 4GB+ RAM available
- 10GB+ disk space

### First Time Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd Lms_project
   ```

2. **Create environment file**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` if needed (default values work for local development)

3. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

4. **In a new terminal, run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Create initial achievements** (optional)
   ```bash
   docker-compose exec web python manage.py shell
   ```
   
   Then run:
   ```python
   from lms.models import Achievement
   
   Achievement.objects.create(
       name="Первые шаги",
       description="Запишитесь на первый курс",
       icon="🎯",
       criteria_type="course_count",
       criteria_value=1,
       points=10
   )
   
   Achievement.objects.create(
       name="Знаток",
       description="Запишитесь на 5 курсов",
       icon="📚",
       criteria_type="course_count",
       criteria_value=5,
       points=50
   )
   
   Achievement.objects.create(
       name="Идеальный результат",
       description="Получите 100% на любом тесте",
       icon="💯",
       criteria_type="test_score",
       criteria_value=100,
       points=25
   )
   
   exit()
   ```

7. **Access the application**
   - Web: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 📱 Access from Other Devices

### On Same Network (Phone, Tablet, Another Computer)

1. **Find your computer's IP address**
   
   Windows:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)
   
   Mac/Linux:
   ```bash
   ifconfig
   ```

2. **Update ALLOWED_HOSTS in .env**
   ```
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,192.168.1.100
   ```
   (Replace with your actual IP)

3. **Restart the web service**
   ```bash
   docker-compose restart web
   ```

4. **Access from other device**
   - Open browser on phone/tablet
   - Navigate to: `http://192.168.1.100:8000`
   - (Replace with your computer's IP)

## 🛠️ Common Commands

### Start services
```bash
docker-compose up
```

### Start in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### View specific service logs
```bash
docker-compose logs -f web
docker-compose logs -f kafka
docker-compose logs -f redis
```

### Restart a service
```bash
docker-compose restart web
```

### Run Django commands
```bash
docker-compose exec web python manage.py <command>
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Check Redis cache
```bash
docker-compose exec redis redis-cli
KEYS *
GET lms:courses:list
```

### Monitor Kafka events
```bash
docker-compose logs -f consumer
```

## 🔧 Troubleshooting

### Port already in use
If you see "port is already allocated":
```bash
# Stop all containers
docker-compose down

# Check what's using the port
netstat -ano | findstr :8000

# Kill the process or change port in docker-compose.yml
```

### Database issues
```bash
# Reset database
docker-compose down -v
docker-compose up --build
docker-compose exec web python manage.py migrate
```

### Kafka not connecting
```bash
# Check Kafka health
docker-compose ps

# Restart Kafka services
docker-compose restart zookeeper kafka
```

### Clear Redis cache
```bash
docker-compose exec redis redis-cli FLUSHALL
```

## 📊 Service URLs

- **Django App**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Kafka**: localhost:9093
- **Zookeeper**: localhost:2181

## 🎯 Testing Features

### Test Redis Caching
1. Visit a course page
2. Check Redis: `docker-compose exec redis redis-cli KEYS '*'`
3. Should see cached course data

### Test Kafka Events
1. Enroll in a course
2. Check consumer logs: `docker-compose logs -f consumer`
3. Should see "course_enrolled" event processed

### Test Achievements
1. Enroll in a course
2. Check profile page
3. Should see "Первые шаги" achievement

## 🚀 Production Deployment

For production, you should:
1. Change `DJANGO_DEBUG=False` in `.env`
2. Set a strong `DJANGO_SECRET_KEY`
3. Use a proper domain in `ALLOWED_HOSTS`
4. Set up SSL/HTTPS
5. Use managed database (not Docker PostgreSQL)
6. Set up monitoring (Prometheus/Grafana)
7. Configure backups

## 📝 Notes

- First startup takes 2-5 minutes (downloading images)
- Subsequent starts are much faster
- Data persists in Docker volumes
- To completely reset: `docker-compose down -v`
