#API/cases/空白/conftest.py
import pytest
from lib.webapi import apimgr

# 将环境初始化为为空白
@pytest.fixture(scope='package', autouse=True)
def st_emptyEnv():
    print(f'\n#### 初始化-删除客户、药品、订单')
    apimgr.mgr_login()
    apimgr.order_del_all()
    apimgr.customer_del_all()
    apimgr.medicine_del_all()

#API/cases/空白/conftest.py/test_客户.py
import  pytest
from lib.webapi import apimgr


# 环境完全空白
class Test_0添删客户1_success:

    def setup_method(self):
        pass

    def teardown_method(self):
        # apimgr.customer_del(self.addedCustomerId)
        apimgr.customer_del_all()

    def test_API_0151(self):
        # '添加客户'
        r = apimgr.customer_add('武汉市桥西医院',
                                '13345679934',
                                "武汉市桥西医院北路")
        addRet = r.json()
        self.addedCustomerId = addRet['id']
        assert addRet['ret'] == 0
        # '检查系统数据'
        r = apimgr.customer_list()
        listRet = r.json()
        expected = {
            "ret": 0,
            "retlist": [
                {
                    "address": "武汉市桥西医院北路",
                    "id": addRet['id'],
                    "name": "武汉市桥西医院",
                    "phonenumber": "13345679934"
                }
            ],
            'total': 1
        }
        assert expected == listRet

    # 此用例不通过
    def test_API_0251(self):
        r = apimgr.customer_del(100000000000)
        editRet = r.json()#出错点：返回的响应r的消息体为html，无法应用json格式
        assert editRet== {
                            "ret": 1,
                            "msg":  "客户ID不存在",
                        }

        # 列出客户
        r = apimgr.customer_list()
        listRet = r.json()
        assert listRet['total'] == 0


class Test_0添改客户1_failure:

    #此用例不通过
    def test_API_0153(self):
        # '添加一个客户'
        r = apimgr.customer_add2({
                            "phonenumber":"13345679934",
                            "address":"南京市鼓楼北路"
                        })
        addRet = r.json()  #出错点：返回的响应r的消息体为html，无法应用json格式
        assert addRet == {
                        "ret": 1,
                        "msg":  "请求消息参数错误",
                    }
        # '检查系统数据'
        r = apimgr.customer_list()
        listRet = r.json()

        assert listRet == {
                    "ret": 0,
                    "retlist": [],
                    'total': 0
                }

    # 此用例不通过
    def test_API_0201(self):
        #修改不存在客户
        r=apimgr.customer_edit(10000000000,
                               {
                                "name":"武汉市桥北医院",
                                "phonenumber":"13345678888",
                                "address":"武汉市桥北医院北路"
                               })
        editRet = r.json()#出错点：返回的响应r的消息体为html，无法应用json格式
        assert editRet == {
            "ret": 1,
            "msg": "客户ID不存在",
        }
        #列出客户
        r = apimgr.customer_list()
        listRet = r.json()
        assert listRet['total']==0


class Test_10添加客户1_success:
    def setup_method(self):
        self.setup_data_customerids=[]
        for i in range(10):
            r = apimgr.customer_add(
                f'武汉市桥西医院_{i + 1}',
                f'100000000{i + 1:02d}',
                f"武汉市桥西医院北路_{i + 1}")
            self.setup_data_customerids.append(r.json()['id'])

    def teardown_method(self):
        for cid in self.setup_data_customerids:
            apimgr.customer_del(cid)
        apimgr.customer_del(self.addedCustomerId)


    def test_API_0152(self):
        #'先列出客户'
        r = apimgr.customer_list()
        listRet1 = r.json()
        customerlist1 = listRet1["retlist"]
        # '添加一个客户'
        r = apimgr.customer_add('南京市鼓楼医院',
                                '13345679934',
                                "南京市鼓楼北路")
        addRet = r.json()
        self.addedCustomerId = addRet['id']
        assert addRet['ret'] == 0
        # 再次列出客户'
        r = apimgr.customer_list(11)
        listRet = r.json()
        expected = {
            "ret": 0,
            "retlist": [
                           {
                               "address": "南京市鼓楼北路",
                               "id": addRet['id'],
                               "name": "南京市鼓楼医院",
                               "phonenumber": "13345679934"
                           }
                       ] + customerlist1,
            'total': 11
        }
        assert expected == listRet


class Test_1修改客户1_success:

    def setup_method(self):
        r = apimgr.customer_add('南京市鼓楼医院',
                                '13345679934',
                                "南京市鼓楼北路")
        addRet = r.json()
        self.addedCustomerId = addRet['id']

    def teardown_method(self):
        # apimgr.customer_del(self.addedCustomerId)
        apimgr.customer_del_all()

    def test_API_0202(self):
        r=apimgr.customer_edit(self.addedCustomerId,
                               {
                                "name":"武汉市桥北医院",
                               })
        editRet = r.json()
        assert editRet['ret'] ==0
        #列出客户
        r = apimgr.customer_list()
        listRet = r.json()
        expected = {
            "ret": 0,
            "retlist": [
                           {
                               "address": "南京市鼓楼北路",
                               "id": self.addedCustomerId,
                               "name": "武汉市桥北医院",
                               "phonenumber":'13345679934'
                           }
                       ],
            'total': 1
        }
        assert expected == listRet

    def test_API_0203(self):
        r = apimgr.customer_edit(self.addedCustomerId,
                                 {
                                     "phonenumber": "13886666666"
                                 })
        editRet = r.json()
        assert editRet['ret'] == 0
        # 列出客户
        r = apimgr.customer_list()
        listRet = r.json()
        expected = {
            "ret": 0,
            "retlist": [
                {
                    "address": "南京市鼓楼北路",
                    "id": self.addedCustomerId,
                    "name": '南京市鼓楼医院',
                    "phonenumber": "13886666666"
                }
            ],
            'total': 1
        }
        assert expected == listRet

    def test_API_0252(self):
        r = apimgr.customer_del(self.addedCustomerId)
        editRet = r.json()
        assert editRet['ret'] == 0
        # 列出客户
        r = apimgr.customer_list()
        listRet = r.json()
        assert listRet['total']==0


#API/cfg/cfg.py
target_host = '127.0.0.1'

#API/lib/webapi.py
import requests
from pprint import pprint
import pytest
import sys
sys.path.append("..")  #..代表上级目录，（"../.."）代表上级目录的上级目录
from cfg import cfg

class APIMgr:
     # 打印操作
    def _printResponse(self,response):
        print('\n\n-------- HTTP response * begin -------')
        print(response.status_code)

        for k,v in response.headers.items():
            print(f'{k}: {v}')

        print('')

        print(response.content.decode('utf8'))
        print('-------- HTTP response * end -------\n\n')

    # 登录操作
    def mgr_login(self,username='byhy',password='88888888',useProxy=False):
        self.s = requests.Session()

        if useProxy:
            self.s.proxies.update({'http': f'http://{cfg.target_host}:8888'})

        response = self.s.post(f"http://{cfg.target_host}/api/mgr/signin",
                                 data={
                                     'username': username,
                                     'password': password
                                 }
                                 )

        self._printResponse(response)
        return response


    # 客户操作
    def customer_list(self,pagesize=10,pagenumber=1,keywords=''):

        print('列出客户')
        response = self.s.get(f"http://{cfg.target_host}/api/mgr/customers",
              params={
                  'action' :'list_customer',
                  'pagesize' :pagesize,
                  'pagenum' :pagenumber,
                  'keywords' :keywords,
              })

        self._printResponse(response)
        return response


    def customer_add(self,name,phonenumber,address):
        print('添加客户')
        response = self.s.post(f"http://{cfg.target_host}/api/mgr/customers",
              json={
                    "action":"add_customer",
                    "data":{
                        "name":name,
                        "phonenumber":phonenumber,
                        "address":address
                    }
                })

        self._printResponse(response)
        return response

    def customer_add2(self,data):
        print('添加客户')
        response = self.s.post(f"http://{cfg.target_host}/api/mgr/customers",
              json={
                    "action":"add_customer",
                    "data":data
                })

        self._printResponse(response)
        return response

    def customer_del(self,cid):
        print('删除客户')
        response = self.s.delete(f"http://{cfg.target_host}/api/mgr/customers",
              json={
                    "action":"del_customer",
                    "id": cid
                })

        self._printResponse(response)
        return response

    def customer_del_all(self):
        response = self.customer_list(100,1)

        theList = response.json()["retlist"]
        for one in theList:
            self.customer_del(one["id"])

    def customer_edit(self,cid,data):
         print('修改客户')
         response=self.s.put(f"http://{cfg.target_host}/api/mgr/customers",
              json={
                    "action":"modify_customer",
                    "id": cid,
                    "newdata":data
                    }        )
         self._printResponse(response)
         return response

    # 药品操作

    def medicine_list(self,pagesize=10,pagenumber=1,keywords=''):
        print('列出药品')
        response = self.s.get(f"http://{cfg.target_host}/api/mgr/medicines",
              params={
                  'action' :'list_medicine',
                  'pagesize' :pagesize,
                  'pagenum' :pagenumber,
                  'keywords' :keywords,
              })

        self._printResponse(response)
        return response



    def medicine_del(self,mid):
        print('删除药品')
        response = self.s.delete(f"http://{cfg.target_host}/api/mgr/medicines",
              json={
                    "action":"del_medicine",
                    "id": mid
                })

        self._printResponse(response)
        return response


    def medicine_del_all(self):
        response = self.medicine_list(100,1)

        theList = response.json()["retlist"]
        for one in theList:
            self.medicine_del(one["id"])


    # 订单操作


    def order_list(self,pagesize=10,pagenumber=1,keywords=''):
        print('列出订单')
        response = self.s.get(f"http://{cfg.target_host}/api/mgr/orders",
              params={
                  'action' :'list_order',
                  'pagesize' :pagesize,
                  'pagenum' :pagenumber,
                  'keywords' :keywords,
              })

        self._printResponse(response)
        return response



    def order_del(self,oid):
        print('删除订单')
        response = self.s.delete(f"http://{cfg.target_host}/api/mgr/orders",
              json={
                    "action":"delete_order",
                    "id": oid
                })

        self._printResponse(response)
        return response


    def order_del_all(self):
        response = self.order_list(100,1)

        theList = response.json()["retlist"]
        for one in theList:
            self.order_del(one["id"])

apimgr = APIMgr()
