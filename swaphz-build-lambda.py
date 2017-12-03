import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:146648089768:swaphz-topic')
    try:
        swaphz_bucket = s3.Bucket('swaphz')
        build_bucket = s3.Bucket('build-swaphz')
    
        swaphz_zip = StringIO.StringIO()  
        build_bucket.download_fileobj('swaphzbuild.zip', swaphz_zip)  
    
        with zipfile.ZipFile(swaphz_zip) as myzip:  
            for nm in myzip.namelist():  
                obj = myzip.open(nm)
                swaphz_bucket.upload_fileobj(obj,nm,ExtraArgs ={'ContentType': mimetypes.guess_type(nm)[0]})
                swaphz_bucket.Object(nm).Acl().put(ACL='public-read')
        topic.publish(Subject="Swaphz", Message="Swaphz code udated")
    except:
        topic.publish(Subject="Swaphz deploy failed", Message="Swaphz code udated failed")
        raise
    return 'Hello from Lambda'
