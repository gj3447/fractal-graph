import random
import time
import db
'''
agent
weight
action
bios 
bios_agnet
bios_weight
environment

---------------------------
value
resource
percent
'''
class agent:
    def __init__(self,id,lv,user):
        #pointer
        self.bios_agent = {}#key = id_bios
        self.weight_up = {}#key = id_agent_up
        self.weight_dn = {}#key = id_agent_dn or id_action
        self.bios = {}
        #static
        self.lv = lv
        self.id = id
        self.user = user
        #variable
        self.resource = float(0)
        self.reward = float(0)
        self.value = float(0)
        self.percent = float(1)
        
    def resource_update(self,agent_list = None,action_list = None):
        self.weight_connect(agent_list = agent_list,action_list = action_list)
        self.resource = float(0)
        self.value = float(0)
        for e in self.bios_agent.values():
            self.resource += e.resource_update(agent_list = agent_list,action_list=action_list)
            self.value += e.value
        return self.resource
    
    def reward_update(self):
        self.reward = float(0)
        for e in self.bios_agent.values():
            self.reward += e.reward_update()
        return self.reward
    
    def weight_change(self,percent,agent =None ,action = None):
        if percent >float(1) or percent < float(0):
            return '''percent overflow'''
        weight_temp
        if agent != None:
            self.weight_connect(agent_list = [agent])
            weight_temp = self.weight_dn[agent.id]
        if action != None:
            self.weight_connect(action_list = [action])
            weight_temp = self.weight_dn[action.id]
        percent_diff = percent - weight_temp.percent
        self_percent = self.percent - percent_diff
        if self_percent>=float(1) or self_percent<=float(0):
            return '''percent overflow'''
        self.percent =self_percent
        weight_temp.percent = percent
        
    def weight_change_list(self,agent_dic=None,action_dic=None):# agent , percent / action , percent
        agent_list = None
        action_list = None
        self_percent = self.percent
        if agent_dic != None:
            agent_list = []
            for e in agent_dic:
                if e['percent']<float(0) or e['percent']>float(1):
                    return '''percent overflow'''
                agent_list.append(e['agent'])
                if e['agent'].id in self.weight_dn.keys():
                    self_percent += self.weight_dn[e['agent'].id].percent - e['percent']
                else:
                    self_percent -= e['percent']
        if action_dic != None:
            action_list = []
            for e in action_dic:
                if e['percent']<float(0) or e['percent']>float(1):
                    return '''percent overflow'''
                action_list.append(e['action'])
                if e['action'].id in self.weight_dn.keys():
                    self_percent += self.weight_dn[e['action'].id].percent - e['percent']
                else:
                    self_percent -= e['percent']
        if self_percent<float(0) or self_percent>float(1):
            return '''percent overflow'''
        self.weight_connect(agent_list=agent_list,action_list=action_list)
        if agent_dic != None:
            for e in agent_dic:
                self.weight_dn[e['agent'].id].percent = e['percent']
        if action_dic != None:
            for e in action_dic:
                self.weight_dn[e['action'].id].percent = e['percent']
        self.percent = self_percent
        return '''success'''
        
    def weight_connect(self,agent_list = None, action_list=None):
        if agent_list != None:
            for e in agent_list :
                if (e.id in self.weight_dn.keys())== False:
                    weight_temp = weight(agent_up = self,agent_dn = e)
        if action_list != None:
            for e in action_list:
                if (e.id in self.weight_dn.keys()) == False:
                    weight_temp = weight(agent_up = self, action = e)
    def printf(self):
        print("agent_up")
        for e in self.weight_up.values():
            print(str(e.agent_up.id)+":"+ str(e.agent_up.resource)+"X"+str(e.percent)+"="+str(e.agent_up.reward))
        print("agent")
        print(str(self.id)+":"+ str(self.resource)+"X"+str(self.percent)+"="+str(self.value))
        print("agent_down")
        for e in self.weight_dn.values():
            if e.agent_dn !=None:
                print(str(e.agent_dn.id)+":"+ str(e.agent_dn.resource)+"X"+str(e.percent)+"="+str(e.agent_dn.reward))
            if e.action !=None:
                print(str(e.action.id)+":"+ str(e.action.value)+"X"+str(e.percent))
class weight:
    def __init__(self,agent_up,agent_dn=None,action=None):
        #pointer
        self.bios_weight = {}#key = id_bios
        self.agent_up = agent_up
        self.agent_dn = agent_dn
        self.action = action
        #variable
        self.percent= float(0)
        #function
        if agent_dn!=None:
            agent_up.weight_dn[agent_dn.id]=self
            agent_dn.weight_up[agent_up.id]=self
        if action != None:
            agent_up.weight_dn[action.id] = self
class action:
    def __init__(self,id,value):
        self.value = value
        self.id = id
class bios:
    def __init__(self,resource,id):
        self.resource = resource
        self.bios_agent = {}#key = agent_name
        self.agent = None
        self.id = id
    def agent_connect(self,agent):
        if self.agent!=None:
            return '''agent connect exist'''
        else:
            self.agent = agent
            agent.bios[self.id] = self
            bios_agent(agent=agent,bios=self,root=True)
    def agent_disconnect(self):
        if self.agent!=None:
            self.agent.bios.pop(self.id)
            for e in self.bios_agent.values():
                e.remove()
            self.agent = None
            self.bios_agent = {}
        else:
            return '''agent connect not exist'''
class bios_agent:
    def __init__(self,agent,bios,root):
        #pointer
        self.bios_weight_up = {}#key = id_agent_up
        self.bios_weight_dn = {}#key = id_agent_dn
        self.agent = agent
        self.bios = bios
        #static
        self.root = root # True of false
        #variable
        self.resource = float(0)
        self.reward = float(0)
        self.value = float(0)
        #function
        agent.bios_agent[bios.id] = self
        bios.bios_agent[agent.id] = self
    def resource_update(self,agent_list = None , action_list= None):
        
        if self.root:
            self.resource = self.bios.resource
        else:
            self.resource = float(0)
            for e in self.bios_weight_up.values():
                self.resource += e.value
        self.value = self.resource * self.agent.percent
        self.bios_weight_connect(agent_list=agent_list,action_list=action_list)
        for e in self.bios_weight_dn.values():
            e.resource_update()
        return self.resource
    
    def reward_update(self):
        self.reward = self.value
        for e in self.bios_weight_dn.values():
            self.reward += e.reward_update()
        if self.root:
            self.bios.resource = self.reward
        return self.reward
    def bios_weight_connect(self,agent_list,action_list):
        if agent_list !=None:
            for e in agent_list:
                if (self.bios.id in e.bios_agent)==False:
                    bios_agent_temp = bios_agent(agent=e,bios=self.bios,root=False)
                if (self.bios.id in self.agent.weight_dn[e.id].bios_weight.keys())==False:
                    bios_weight_temp = bios_weight(bios_agent_up = self,bios_agent_dn=e.bios_agent[self.bios.id],weight=self.agent.weight_dn[e.id],bios=self.bios)
        if action_list !=None:
            for e in action_list:
                if (self.bios.id in self.agent.weight_dn[e.id].bios_weight.keys())==False:
                    bios_weight_temp = bios_weight(bios_agent_up = self,weight=self.agent.weight_dn[e.id],bios=self.bios)
    def remove(self):
        if self.bios.id in self.agent.bios_agent.keys():
            self.agent.bios_agent.pop(self.bios.id)
        for e in self.bios_weight_dn.values():
            e.remove()
class bios_weight:
    def __init__(self,bios_agent_up,weight,bios,bios_agent_dn=None):
        #pointer
        self.bios_agent_up = bios_agent_up;
        self.bios_agent_dn = bios_agent_dn;
        self.weight = weight
        self.bios = bios
        #barialbe
        self.value = float(0)
        self.action_value = float(0)
        #function
        if bios_agent_dn !=None:
            bios_agent_dn.bios_weight_up[bios_agent_up.agent.id] = self
            bios_agent_up.bios_weight_dn[bios_agent_dn.agent.id] = self
        if weight.action != None:
            bios_agent_up.bios_weight_dn[weight.action.id] = self
        self.weight.bios_weight[bios.id] = self

    def resource_update(self):
        self.value = self.bios_agent_up.resource * self.weight.percent
        if self.weight.action !=None:
            self.action_value = self.value/self.weight.action.value
        return self.value
    
    def reward_update(self):
        if self.weight.action != None:
            self.value = self.weight.action.value * self.action_value
        if self.bios_agent_dn!=None:
            self.value = (self.value/ self.bios_agent_dn.resource) * self.bios_agent_dn.reward
        return self.value
    
    def remove(self):
        if self.bios.id in self.weight.bios_weight.keys():
            self.weight.bios_weight.pop(self.bios.id)
        
class environment:
    def __init__(self):
        self.agent = {} # key = id_agent
        self.action = {} # key = id_action
        self.agent_lv = {int(0):[]}
        self.bios = {} # key = id_bios
        
    def bios_create(self,id,resource): # bios 생성
        if id in self.bios.keys():
            return '''id_bios is exist'''
        else:
            bios_temp = bios(id=id,resource=resource)
            self.bios[id] = bios_temp
            
    def bios_connect(self,id_bios,id_agent): # bios 를 agent 에 연결
        self.bios[id_bios].agent_disconnect()
        self.bios[id_bios].agent_connect(self.agent[id_agent])
        
    def agent_create(self,id,lv): # agent 생성
        if id in self.agent.keys():
            return '''id_agent is exist'''
        else:
            agent_temp = agent(id=id,lv=lv)
            self.agent[id] = agent_temp
            if (lv in self.agent_lv.keys()) == False:
                self.agent_lv[lv] = []
            self.agent_lv[lv].append(agent_temp)
            
    def agent_printf(self,id_agent):
        self.agent[id_agent].printf()
        
    def action_create(self,id,value): # action 생성
        if id in self.action.keys():
            return '''id_action is exist'''
        else:
            action_temp = action(id=id,value=value)
            self.action[id] = action_temp
            
    def action_change(self,id,value):
        self.action[id],value = value
        
    def action_change_list(self,action_dic): # id, value 
        for e in action_dic:
            self.action[e['id']].value = e['value']
            
    def weight_change_list(self,id_agent,weight_dic): #id, percent
        agent_temp = self.agent[id_agent]
        if agent_temp.lv == 0:
            action_dic = []
            for e in weight_dic:
                dic_temp = {'action':self.action[e['id']],'percent':e['percent']}
                action_dic.append(dic_temp)
            agent_temp.weight_change_list(action_dic = action_dic)
        else:
            agent_dic = []
            for e in weight_dic:
                dic_temp = {'agent':self.agent[e['id']],'percent':e['percent']}
                agent_dic.append(dic_temp)
            agent_temp.weight_change_list(agent_dic = agent_dic)
    
    def weight_change(self,id_agent,id,percent):
        agent_temp = self.agent[id_agent]
        if agent_temp.lv == int(0):
            agent_temp.weight_change(action=self.action[id],percent=percent)
        else:
            agent_temp.weight_change(action=self.agent[id],percent=percent)
            
    def weight_random(self,id_agent):
        agent_temp = self.agent[id_agent]
        if agent_temp.lv == 0:
            action_list = []
            action_dic = []
            value_sum = random.random()
            for e in self.action.values():
                value_random = random.random()
                action_list.append([e.id,value_random])
                value_sum += value_random
            for e in action_list:
                action_dic.append({'action':self.action[e[0]],'percent':float(e[1]/value_sum)})
            return agent_temp.weight_change_list(action_dic = action_dic)
        else:
            agent_list = []
            agent_dic = []
            value_sum = random.random()
            for e in self.agent_lv[int(agent_temp.lv-1)]:
                value_random = random.random()
                agent_list.append([e.id,value_random])
                value_sum += value_random
            for e in agent_list:
                agent_dic.append({'agent':self.agent[e[0]],'percent':float(e[1]/value_sum)})
            return agent_temp.weight_change_list(agent_dic = agent_dic)
            
    def resource_update(self):
        for e in range(self.lv_max(),-1,-1):
            if e in self.agent_lv.keys():
                for a in self.agent_lv[e]:
                    if e == int(0):
                        a.resource_update(action_list = self.action.values())
                    else:
                        a.resource_update(agent_list = self.agent_lv[int(e-1)])
                    
    def reward_update(self):
        for e in range(0,self.lv_max()+1,1):
            if e in self.agent_lv.keys():
                for a in self.agent_lv[e]:
                    a.reward_update()
                    
    def printf(self):
        print('-----Fractal Machine Learning Environment-----')
        for e in range(self.lv_max(),-1,-1):
            print("Lv "+str(e))
            for a in self.agent_lv[e]:
                if a.resource == float(0):
                    print(str(a.id)+":"+str(a.reward)+"/"+str(a.resource)+"=0.00%")
                else:
                    print(str(a.id)+":"+str(a.reward)+"/"+str(a.resource)+"="+str((a.reward-a.resource)/a.resource)+"%")
        print("Action")
        for e in self.action.values():
            print(str(e.id)+":"+str(e.value)+" ",end="")
        print("")
        print("Bios")
        for e in self.bios.values():
            print(str(e.id)+": resource="+str(e.resource),end="")
            if e.agent!=None:
                print(" agent="+str(e.agent.id))
            else:
                print("")
        
    def lv_max(self):
        result = int(0)
        for e in self.agent_lv.keys():
            if e> result:
                result = e
        return result
    
    def update(self):
        agent_list = db.agent_list()
        weight_list = db.weight_list()
        bios_list = db.bios_list()
        
class interpreter:
    def __init__(self,environment = None,command_mode = False):
        print("interpreter start")
        self.environment = environment
        self.tocken = []
        self.func_dic = {
            "printf":self.printf, # 출력 {agent=id_agent}
            "sleep":self.sleep, # 잠시쉬기 {time=float}
            "agent_create":self.agent_create, # agent 생성 {id,lv,random}
            "action_create":self.action_create, # action 생성 {id,value}
            "bios_create":self.bios_create, # bios 생성 {id,resource}
            "bios_connect":self.bios_connect, # bios 연결 {id_bios,id_agent}
            "action_change":self.action_change, # action value 변경 {id_action=value}
            "weight_change":self.weight_change, # weight percent 변경 {agent,id_agent=percent}
            "resource_update":self.resource_update, # 전체 그래프 resource 
            "reward_update":self.reward_update #{}
            
        }
        if command_mode:
            self.input_command()
            
    def input_command(self):
        while True:
            line = input()
            if line=="exit":
                return
            self.input_line(line=line)
            
    def input_line(self,line):
        tocken = self.slice(string=line,char ='|')
        for e in tocken:
            self.tocken.append(e)
        self.tocken_function()
        
    def tocken_function(self):
        while len(self.tocken)>0:
            tocken = self.tocken.pop(0)
            tocken_bios = self.binary(string = tocken,char=":")
            func = tocken_bios[0]
            command_line = tocken_bios[1]
            if func in self.func_dic.keys():
                self.func_dic[func](command_line=command_line)
    
    def printf(self,command_line): # 쓰기
        if command_line == "":
            self.environment.printf()
            return

        command_dic = self.command_dic(command_line=command_line)
        if 'agent' in command_dic.keys():
            self.environment.agent_printf(id_agent=str(command_dic['agent']))
            return
        print(command_line)
        
    def sleep(self,command_line):
        if command_line =="":
            time.sleep(1)
            return
        command_dic = self.command_dic(command_line=command_line)
        if 'time' in command_dic.keys():
            time.sleep(float(command_dic['time']))
            
    def agent_create(self,command_line): # agent 생성
        command_dic = self.command_dic(command_line=command_line)
        random = False
        if ('id' in command_dic.keys())==False:
            return '''command error'''
        if ('lv' in command_dic.keys())==False:
            return '''command error'''
        if 'random' in command_dic.keys():
            random = True
        self.environment.agent_create(lv=int(command_dic['lv']),id=str(command_dic['id']))
        if random:
            result=  self.environment.weight_random(id_agent=str(command_dic['id']))
            print("agent_create_random" + str(result))
        else:
            print("agent_create")
    
    def bios_create(self,command_line): # bios 생성
        command_dic = self.command_dic(command_line=command_line)
        if ('id' in command_dic.keys())==False:
            return '''command error'''
        if ('resource' in command_dic.keys())==False:
            return '''command error'''
        self.environment.bios_create(id=str(command_dic['id']),resource=float(command_dic['resource']))
        print("bios_create")
        
    def bios_connect(self,command_line): # bios 연결
        command_dic = self.command_dic(command_line=command_line)
        if ('id_bios' in command_dic.keys())==False:
            return '''command error'''
        if ('id_agent' in command_dic.keys()) == False:
            return '''command error'''
        self.environment.bios_connect(id_bios=command_dic['id_bios'],id_agent=command_dic['id_agent'])
        print("bios_connect")
        
    def weight_change(self,command_line): # weight 변경
        command_dic = self.command_dic(command_line=command_line)
        id_agent = ""
        if ('agent' in command_dic.keys())==False:
            return '''command error'''
        else:
            id_agent = command_dic.pop('agent')
        if 'random' in command_dic.keys():
            self.environment.weight_random(id_agent = str(id_agent))
            print("weight_random")
            return
        else:
            weight_dic = []
            for e in command_dic.keys():
                weight_dic.append({"id":str(e),"percent":float(weight_dic[e])})
            self.environment.weight_change_list(id_agent=str(id_agent),weight_dic = weight_dic)
            print("weight_change")
            return
        
    def action_create(self,command_line): # action 생성
        command_dic = self.command_dic(command_line=command_line)
        if ('id' in command_dic.keys())==False:
            return '''command error'''
        if ('value' in command_dic.keys())==False:
            return '''command error'''
        self.environment.action_create(id=str(command_dic['id']),value=float(command_dic['value']))
        print("action_create")
        
    def action_change(self,command_line): # action 변경
        command_dic = self.command_dic(command_line=command_line)
        action_dic = []
        for e in command_dic.keys():
            action_dic.append({'id':str(e),'value':float(command_dic[e])})
        self.environment.action_change_list(action_dic=action_dic)
        print("action_change")
        
    def resource_update(self,command_line):
        self.environment.resource_update()
        print("resource_update")
        
    def reward_update(self,command_line):
        self.environment.reward_update()
        print("reward_update")
    
    def command_dic(self,command_line):
        command = self.slice(string=command_line,char=",")
        result = {}
        for e in command:
            binary = self.binary(string = e,char="=")
            result[binary[0]] = binary[1]
        return result
    
    def slice(self,string,char):
        result = []
        buffer = ""
        for e in string:
            if e == char:
                result.append(buffer)
                buffer = ""
            else:
                buffer += e
        result.append(buffer)
        return result
    
    def binary(self,string,char):
        result = []
        buffer = ""
        slice = False
        for e in string:
            if slice:
                buffer += e
            else:
                if e == char:
                    result.append(buffer)
                    buffer = ""
                    slice = True
                else:
                    buffer += e
        if slice:
            result.append(buffer)
        else:
            result.append(buffer)
            result.append("")
        return result
    
if __name__=="__main__":
    env = environment()
    ip = interpreter(environment=env,command_mode= True)
