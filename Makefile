all: package

clean:
	mvn clean

test: clean
	mvn test

package: clean
	mvn package

run: clean package
	docker-compose up -d
	java -jar -Dspring.profiles.active=local target/stockreader-0.0.1.jar

deploy:
	java -jar -Dspring.profiles.active=prod target/stockreader-0.0.1.jar
