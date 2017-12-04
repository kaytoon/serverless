import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:146648089768:swaphz-topic')
    location = {

        "bucketName": 'build-swaphz',
            
        "objectKey": 'swaphzbuild.zip'
            
     }
    try:
        swaphz_bucket = s3.Bucket('swaphz')
        build_bucket = s3.Bucket(location["bucketName"])
        swaphz_zip = StringIO.StringIO()  
        build_bucket.download_fileobj(location["objectKey"], swaphz_zip)
        
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                     location = artifact["location"]["s3Location"]
        print "Building portfolio from " + str(location)
        
        with zipfile.ZipFile(swaphz_zip) as myzip:  
            for nm in myzip.namelist():  
                obj = myzip.open(nm)
                swaphz_bucket.upload_fileobj(obj,nm,ExtraArgs ={'ContentType': mimetypes.guess_type(nm)[0]})
                swaphz_bucket.Object(nm).Acl().put(ACL='public-read')
        topic.publish(Subject="Swaphz", Message="Swaphz code udated")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Swaphz deploy failed", Message="Swaphz code udated failed")
        raise
    return 'Hello from Lambda'
