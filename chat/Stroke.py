from py2neo import Graph, Node, Relationship
#一、查询
def reason(input):#查询致病原因
    #连接数据库
    directorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    #查找节点
    cypher_text ="""
        MATCH (n:reason)-[:cause]->(m:illness{{cn:'{first_name}'}})  RETURN n.reason order by n.id asc
        """.format(first_name=input)
    result =directorGraph.run(cypher_text)
    return result

def pm(input):#查询预防措施
    #连接数据库
    directorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    #查找节点
    cypher_text ="""
        MATCH (m:illness{{cn:'{first_name}'}})-[:prevention]->(n:pmeasure)  RETURN n.pmeasure order by n.id asc
        """.format(first_name=input)
    result =directorGraph.run(cypher_text)
    return result

#二、修改/更新（对节点的属性值进行修改）
def Modify(entity,entity1,entity2,entity3):
    #连接数据库
    directorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    #查找节点
    #match (s:'{first_name}') where s.'{s_name}'='{p_name}'  set s.'{s_name}'='{v_name}' return s.'{s_name}'
    cypher_text ="""
        match (s:{first_name}) where s.{s_name}='{p_name}'  set s.{s_name}='{v_name}' return s.{s_name}
        """.format(first_name=entity,s_name=entity1,p_name=entity2,v_name=entity3)
    result =directorGraph.run(cypher_text)
    return result


#三、删除/增加（指定节点）
#3.1新增特定节点及关系（测试：尝试新增一条新的预防措施）
#对脑出血新增一条预防措施
def nadd(entity,entity1):#难点，由于新建节点时，Cypher语句中自带{}，单单用format 格式化函数无法完成，因为format总是回去识别例如：
    # CREATE (m:Person{name:*,title:*}) return m中自带的大括号{}，所以需要结合格式化输出%s才能完成任务。
    #连接数据库
    directorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    #新增节点
    #CREATE (n:pmeasure{id:{a},name:pm,pmeasure:'{p_name}'}) return n
    #CREATE (m:Person{name:*,title:*}) return m
    #cypher_text ="""title:'{a}',name:'{b}'""".format(a=entity,b=entity1)
    cypher_text ="""id:{a},name:'pm',pmeasure:'{p}'""".format(a=entity,p=entity1)
    directorGraph.run("CREATE (m:pmeasure {%s}) return m" % cypher_text)
    directorGraph.run("MATCH (n:illness),(p:pmeasure) WHERE n.id =22 AND p.id={a} CREATE (n)-[r:prevention] -> (p) RETURN r".format(a=entity))
    # node1 = Node("Person",name = entity,title=entity1) 
    # directorGraph.create(node1)
    # directorGraph.run(cypher_text)a



#3.2删除特定节点及关系
#删除脑出血的一条预防措施（包括节点和关系）
def delete(entity):
    #连接数据库
    directorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    #新增节点
    a_text ="""
        MATCH (n:illness),(p:pmeasure) WHERE n.id =22 AND p.id={first_name} optional match (n)-[r]->(p) delete r
        """.format(first_name=entity)
    d_text ="""
        match (n:pmeasure) where n.id={first_name}   delete n
        """.format(first_name=entity)        
    directorGraph.run(a_text)
    directorGraph.run(d_text)
    # node1 = Node("Person",name = entity,title=entity1) 
    # directorGraph.create(node1)
    # directorGraph.run(cypher_text)a
    #match (n:Person) where n.name='李白'   delete n
    # MATCH (n:illness),(p:pmeasure)
    # WHERE n.id =22 AND p.id=
    # CREATE (n)-[r:prevention]->(p)
    # RETURN r





