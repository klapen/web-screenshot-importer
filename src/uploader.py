import boto3

s3 = boto3.resource('s3')

BUCKET_NAME = 'eyequant-de'

def send_image(filename, binary_data):
    try:
        obj = s3.Object(BUCKET_NAME, filename)
        obj.put(Body=binary_data, ACL='public-read')
        location = boto3.client('s3').get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
        return "https://s3-%s.amazonaws.com/%s/%s" % (location, BUCKET_NAME, filename)
    except Exception as err:
        print('upload_image - Error saving on bucket %s: %s' % (BUCKET_NAME, err))
        return ''

