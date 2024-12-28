# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Grant execute permissions to the mvnw script
RUN chmod +x ./mvnw

# Run Maven to build the project
RUN ./mvnw clean package

# Expose the port that the app runs on
EXPOSE 8080

# Run the jar file
ENTRYPOINT ["java", "-jar", "target/spring-boot-middleware-0.0.1-SNAPSHOT.jar"]
