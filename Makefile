all: clean package

clean:
	mvn clean

test:
	mvn test

package:
	mvn package

run:
	java -jar -Dspring.profiles.active=local target/stockreader-0.0.1.jar

deploy:
	java -jar -Dspring.profiles.active=prod target/stockreader-0.0.1.jar
