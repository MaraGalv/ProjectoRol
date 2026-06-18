FROM python:alpine

WORKDIR /app

# Install dos2unix - Essential for converting Windows line endings in shell scripts
RUN apk add --no-cache dos2unix

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Convert line endings of the script to Unix format
RUN dos2unix run_tests.sh

RUN chmod +x run_tests.sh

CMD ["sh", "-c", "./run_tests.sh"]