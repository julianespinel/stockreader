all: package

clean:
	mvn clean

test:
	mvn clean test

package:
	mvn clean package

run:
	docker-compose up -d
	java -jar -Dspring.profiles.active=local target/stockreader-0.0.1.jar

deploy:
	java -jar -Dspring.profiles.active=prod target/stockreader-0.0.1.jar
