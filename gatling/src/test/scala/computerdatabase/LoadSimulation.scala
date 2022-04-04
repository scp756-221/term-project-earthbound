package computerdatabase

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class LoadSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("http://acd3cf27a90a347b0a824697ad0fc8e7-1926073645.us-west-2.elb.amazonaws.com:80") // Here is the root for all relative URLs
    .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8") // Here are the common headers
    .acceptEncodingHeader("gzip, deflate")
    .acceptLanguageHeader("en-US,en;q=0.5")
    .userAgentHeader("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0")

  val scn = scenario("s1 s2 s3 request") // A scenario is a chain of requests and pauses
    .exec(http("s2 request getall")
      .get("/api/v1/music/")
      .header("""Authorization""", """bigG"""))
    .pause(2) // Note that Gatling has recorded real time pauses
    .exec(http("s2 request getid")
      .get("/api/v1/music/22e47f97-11ca-4c3c-8e77-f3068fddaf6e")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s2 request test")
      .get("/api/v1/music/test")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s2 request health")
      .get("/api/v1/music/health")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s3 request getall")
      .get("/api/v1/songs_list/obtainall")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s3 request getid")
      .get("/api/v1/songs_list/obtain/26e6462c-eacf-40bb-b4d0-d683966e2624")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s3 health request")
      .get("/api/v1/health")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s1 request getid")
      .get("/api/v1/user/423a10a6-ab66-48c5-a1c7-dffb3169d744")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s1 request getall")
      .get("/api/v1/user/")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s1 request health")
      .get("/api/v1/user/health")
      .header("""Authorization""", """bigG"""))
    .pause(2)
    .exec(http("s1 request readiness")
      .get("/api/v1/user/readiness")
      .header("""Authorization""", """bigG"""))
    .pause(2)


  setUp(scn.inject(
      atOnceUsers(2),
      rampUsers(2) during(5)
  ).protocols(httpProtocol))
}
