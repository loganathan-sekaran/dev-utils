
pom_changes_dict={
"<maven.compiler.source>11</maven.compiler.source>" : "<maven.compiler.source>21</maven.compiler.source>",
"<maven.compiler.target>11</maven.compiler.target>" : "<maven.compiler.target>21</maven.compiler.target>",
"1.2.1-SNAPSHOT" : "1.2.1-java21-SNAPSHOT"
}

java_file_changes_dict={
"javax.servlet.http.HttpServletRequest" : "jakarta.servlet.http.HttpServletRequest",
"javax.servlet.http.HttpServletRespons" : "jakarta.servlet.http.HttpServletResponse",
"javax.servlet.http.ServletException" : "jakarta.servlet.http.ServletException",
"javax.servlet.http.Cookie" : "jakarta.servlet.http.Cookie",
"javax.servlet.FilterChain" : "jakarta.servlet.FilterChain",
"javax.annotation.PostConstruct" : "jakarta.annotation.PostConstruct",
"javax.activation.DataSource" : "jakarta.activation.DataSource",
"javax.persistence.EntityManagerFactory" : "jakarta.persistence.EntityManagerFactory",

"javax.persistence.Column" : "jakarta.persistence.Column",
"javax.persistence.Entity" : "jakarta.persistence.Entity",
"javax.persistence.Id" : "jakarta.persistence.Id",
"javax.persistence.Table" : "jakarta.persistence.Table",
"javax.validation.constraints.NotNull" : "jakarta.validation.constraints.NotNull",
"javax.validation.constraints.Size" : "jakarta.validation.constraints.Size",

"javax.validation.ConstraintViolation" : "jakarta.validation.ConstraintViolation",
"javax.validation.Validation" : "jakarta.validation.Validation",
"javax.validation.Validator" : "jakarta.validation.Validator",
"javax.validation.ValidatorFactory" : "jakarta.validation.ValidatorFactory",

"org.apache.http.impl.classic.HttpClientBuilder": "org.apache.hc.client5.http.impl.classic.HttpClientBuilder",
"org.apache.http.impl.classic.HttpClients" : "org.apache.hc.client5.http.impl.classic.HttpClients",
"org.apache.http.conn.ssl.SSLConnectionSocketFactory" : "org.apache.hc.client5.http.ssl.SSLConnectionSocketFactory"
}

docker_file_changes_dict= {

"FROM openjdk:11"  : "FROM openjdk:21"

}

push_trigger_changes_dict= {

"java-version: 11" : "java-version: 21"

}