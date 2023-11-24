
class Obj(object):
    def __init__(self, filename):
        with open(filename,"r") as file:
            self.lines = file.read().splitlines()
        
        self.objData = []
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        self.parse()
        self.construccion()

        
    def parse(self):
        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue
        
            if prefix =="v": #Vertices
               self.vertices.append(list(map(float, list(filter(None,value.split(" "))))))
            elif prefix =="vt": #Texture coordinates
               self.texcoords.append(list(map(float, list(filter(None,value.split(" "))))))
            elif prefix =="vn": #Normals
               self.normals.append(list(map(float, list(filter(None,value.split(" "))))))
            elif prefix == "f": #Faces
                self.faces.append([list(map(int, list(filter(None,vert.split("/"))))) for vert in list(filter(None,value.split(" ")))])
    
    def construccion(self):
        for face in self.faces:
            #Triangulos
            if len(face) == 3:
                for vertexInfo in face:
                    vertexID, texcoordID, normalID = vertexInfo
                    vertex = self.vertices[vertexID - 1]
                    normals = self.normals[normalID - 1]
                    uv = self.texcoords[texcoordID - 1]
                    uv = [uv[0], uv[1]]
                    self.objData.extend(vertex + uv + normals)
            #Cuadrados
            elif len(face) == 4:
                for i in [0, 1, 2]:
                    vertexInfo = face[i]
                    vertexID, texcoordID, normalID = vertexInfo
                    vertex = self.vertices[vertexID - 1]
                    normals = self.normals[normalID - 1]
                    uv = self.texcoords[texcoordID - 1]
                    uv = [uv[0], uv[1]]
                    self.objData.extend(vertex + uv + normals)
                for i in [0, 2, 3]:
                    vertexID, texcoordID, normalID = vertexInfo
                    vertex = self.vertices[vertexID - 1]
                    normals = self.normals[normalID - 1]
                    uv = self.texcoords[texcoordID - 1]
                    uv = [uv[0], uv[1]]
                    self.objData.extend(vertex + uv + normals)
                