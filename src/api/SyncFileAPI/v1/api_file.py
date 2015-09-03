from . import file_manage
from .models import UserAuthID, FileSys

def create_basic_json_response(error_code, msg, status):
	json_response = {}
	json_response['error_code'] = error_code
	json_response['msg'] = msg
	json_response['status'] = status
	return json_response

def upload_file(request):
	req_auth_id = request.GET.get('authid', '')
	req_username = UserAuthID.objects.filter(authID = req_auth_id)[0].userName
	req_file_path = request.GET.get('filepath', '')
	file_path = '{0}\\{1}'.format(req_username, req_file_path)
	
	mgr = file_manage.fileManage()
	
	content_type_httpheader = request.META.get('CONTENT_TYPE')#get http header parameter from client
	content_type = content_type_httpheader.split(';')[0]
	
	if(content_type != 'text/plain'):#post request from html form element
		post_data_split_len = len(request.body.decode('utf-8').split('\r\n'))
		boundary_begin = request.body.decode('utf-8').split('\r\n')[0]
		boundary_end = request.body.decode('utf-8').split('\r\n')[post_data_split_len-2]
		file_data = ''.join(request.body.decode('utf-8').split('\r\n')[4:post_data_split_len-2])
		#print('post_data_split_len:{0}'.format(post_data_split_len))
		#print('boundary_begin:{0}'.format(boundary_begin))
		#print('boundary_end:{0}'.format(boundary_end))
		#print('file_data:{0}'.format(file_data))
		response_data = 'post from form'
		#stat = mgr.create_file(file_path, file_data)
		#print(stat)
	else:#if the post request from pure post, the request.body is file content
		response_data = 'post from pure post'
	return response_data
	
def api_file(request):
	'''authid should be validated before this function'''
	response_data = 'file op'
	req_op = request.GET.get('op', '')
	if(request.method == 'POST'):
		if(req_op == 'upload'):
			response_data = upload_file(request)
		else:
			response_data = create_basic_json_response(1201, 'not support this op', 'error')
		
	return response_data