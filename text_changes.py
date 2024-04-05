
pom_changes_dict={
"<maven.compiler.source>11</maven.compiler.source>" : "<maven.compiler.source>21</maven.compiler.source>",
"<maven.compiler.target>11</maven.compiler.target>" : "<maven.compiler.target>21</maven.compiler.target>",
"1.2.1-SNAPSHOT" : "1.2.1-java21-SNAPSHOT",
"<jacoco.maven.plugin.version>0.8.5</jacoco.maven.plugin.version>" : "<jacoco.maven.plugin.version>0.8.11</jacoco.maven.plugin.version>"
}

java_file_changes_dict={
"javax.servlet." : "jakarta.servlet.",
"javax.annotation." : "jakarta.annotation.",
"javax.activation." : "jakarta.activation.",
"javax.persistence." : "jakarta.persistence.",
"javax.validation." : "jakarta.validation.",
"javax.mail." : "jakarta.mail.",

"org.apache.http.impl.client." : "org.apache.hc.client5.http.impl.classic.",
"org.apache.http.conn.ssl.SSLConnectionSocketFactory" : "org.apache.hc.client5.http.ssl.SSLConnectionSocketFactory"

}

docker_file_changes_dict= {

"FROM openjdk:11"  : "FROM eclipse-temurin:21-jre-alpine",
"apt-get -y update" : "apk -q update",
"apt-get update -y" : "apk -q update",
"apt-get install -y" : "apk add -q",
"apt-get -y install" : "apk add -q",
"groupadd -g ${container_user_gid} ${container_user_group}" : 'addgroup -g ${container_user_gid} ${container_user_group}',
"useradd -u ${container_user_uid} -g ${container_user_group} -s /bin/sh -m ${container_user}" : 'adduser -s /bin/sh -u ${container_user_uid} -G ${container_user_group} -h /home/${container_user} --disabled-password ${container_user}',

'ARG container_user_uid=1001' : 'ARG container_user_uid=1002'

}

push_trigger_changes_dict= {

"java-version: 11" : "java-version: 21"

}

kernel_bom_dependency_xml = """
			<dependency>
				<groupId>io.mosip.kernel</groupId>
				<artifactId>kernel-bom</artifactId>
				<version>1.2.1-java21-SNAPSHOT</version>
				<type>pom</type>
				<scope>import</scope>
			</dependency>
        """
        