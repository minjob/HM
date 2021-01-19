<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">可视化建表</span>
      </div>
      <div class="platformContainer">
        <el-col :span="4" class="marginBottom">
          <el-card class="box-card text-center">
            <i class="el-icon-circle-plus-outline text-size-24" @click="CreateTableDialogVisible = true"></i>
          </el-card>
        </el-col>
        <el-col :span="4" v-for="(item,index) in TableList" :key="index" class="marginBottom">
          <el-card class="box-card" :body-style="{padding:'20px 20px 50px',height:'200px'}">
            <div slot="header" class="text-size-14">
              <p>{{ item.TableName }}-{{ item.TableDescrip }}</p>
            </div>
            <div class="scrollable">
              <p v-for="(field,fieldIndex) in item.FieldList" class="text-size-12 marginBottom-5" :key="fieldIndex">
                 {{ field.FieldName }} {{ field.TitleName }}
                <span class="el-icon-remove-outline floatRight cursor-pointer color-red" @click="removeField(item.ID)"></span>
              </p>
            </div>
            <div style="line-height: 50px;border-top: 1px solid #eee;text-align: center;">
              <p>
                <el-button size="mini" type="primary" icon="el-icon-plus" circle @click="addField(item.TableName)"></el-button>
                <el-button size="mini" type="danger" icon="el-icon-minus" circle @click="removeTable(item.ID)"></el-button>
                <el-button size="mini" type="success" icon="el-icon-check" circle></el-button>
              </p>
            </div>
          </el-card>
        </el-col>
      </div>
      <el-dialog title="建表" :visible.sync="CreateTableDialogVisible" width="40%">
        <el-form :model="CreateTableField">
          <el-form-item label="表名">
            <el-input v-model="CreateTableField.TableName"></el-input>
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="CreateTableField.TableDescrip"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="CreateTableDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveCreateTable">保存</el-button>
        </span>
      </el-dialog>
      <el-dialog title="添加字段" :visible.sync="FieldSetDialogVisible" width="40%" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="CreateFieldListField" label-width="110px">
          <el-form-item label="表名">
            <el-input v-model="CreateFieldListField.TableName" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="字段名称">
            <el-input v-model="CreateFieldListField.TitleName"></el-input>
          </el-form-item>
          <el-form-item label="字段">
            <el-input v-model="CreateFieldListField.FieldName"></el-input>
          </el-form-item>
          <el-form-item label="VARCHAR长度">
            <el-input v-model="CreateFieldListField.length"></el-input>
          </el-form-item>
          <el-form-item label="字段类型">
            <el-input v-model="CreateFieldListField.type"></el-input>
          </el-form-item>
          <el-form-item label="字段注释">
            <el-input v-model="CreateFieldListField.comment"></el-input>
          </el-form-item>
          <el-form-item label="是否为主键">
            <el-input v-model="CreateFieldListField.primarykey"></el-input>
          </el-form-item>
          <el-form-item label="是否自增">
            <el-input v-model="CreateFieldListField.autoincrement"></el-input>
          </el-form-item>
          <el-form-item label="是否为空">
            <el-input v-model="CreateFieldListField.nullable"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="FieldSetDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveFieldSet">保存</el-button>
        </span>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "BuildTable",
    data(){
      return {
        TableList:[],
        CreateTableDialogVisible:false,
        CreateTableField:{
          TableName:"",
          TableDescrip:""
        },
        FieldList:[],
        CreateFieldListField:{
          TableName:"",
          TitleName:"",
          FieldName:"",
          length:"",
          type:"",
          comment:"",
          primarykey:"",
          autoincrement:"",
          nullable:"",
        },
        FieldSetDialogVisible:false,
      }
    },
    mounted(){
      this.getTable()
    },
    methods:{
      getTable(){
        var that = this
        var params = {
          tableName: "CreateTableSet",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.TableList = []
            that.TableList = res.data.data.rows
            that.getFieldSet()
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      saveCreateTable(){
        var that = this
        if(that.CreateTableField.TableName || that.CreateTableField.TableDescrip){
          var params = {
            tableName:"CreateTableSet",
            TableName:this.CreateTableField.TableName,
            TableDescrip:this.CreateTableField.TableDescrip,
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res => {
            if(res.data.code === "200"){
              this.$message({
                type:'success',
                message:res.data.message
              })
              this.CreateTableDialogVisible = false
              this.getTable()
            }else{
              that.$message({
                type: 'info',
                message: res.data.message
              });
            }
          })
        }else{
          that.$message({
            type: 'info',
            message: "表单不可为空"
          });
        }
      },
      getFieldSet(){
        var that = this
        var params = {
          tableName: "FieldSet",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.TableList.forEach(i =>{
              i.FieldList = []
              res.data.data.rows.forEach(item =>{
                if(i.TableName === item.TableName){
                  i.FieldList.push(item)
                }
              })
            })
            that.$set(that.TableList)
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      addField(TableName){
        this.FieldSetDialogVisible = true
        this.CreateFieldListField.TableName = TableName
      },
      // 删除表
      removeTable(id){
        var mulId = [{id:id}]
        var params = {
          tableName:"CreateTableSet",
          delete_data:JSON.stringify(mulId)
        }
        this.$confirm('确定删除所选记录？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {
          this.axios.delete("/api/CUID",{
            params: params
          }).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.getTable()
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      saveFieldSet(){
        var that = this
        var params = {
          tableName:"FieldSet",
          TableName:this.CreateFieldListField.TableName,
          TitleName:this.CreateFieldListField.TitleName,
          FieldName:this.CreateFieldListField.FieldName,
          length:this.CreateFieldListField.length,
          type:this.CreateFieldListField.type,
          comment:this.CreateFieldListField.comment,
          primarykey:this.CreateFieldListField.primarykey,
          autoincrement:this.CreateFieldListField.autoincrement,
          nullable:this.CreateFieldListField.nullable,
        }
        this.axios.post("/api/CUID",this.qs.stringify(params)).then(res => {
          if(res.data.code === "200"){
            this.$message({
              type:'success',
              message:res.data.message
            })
            this.FieldSetDialogVisible = false
            this.getTable()
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //删除字段
      removeField(id){
        var that = this
        var mulId = [{id:id}]
        var params = {
          tableName:"FieldSet",
          delete_data:JSON.stringify(mulId)
        }
        this.$confirm('确定删除所选记录？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {

          this.axios.delete("/api/CUID",{
            params: params
          }).then(res =>{
            if(res.data.code === "200"){
              that.$message({
                type: 'success',
                message: res.data.message
              });
              that.getTable()
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      }
    }
  }
</script>

<style scoped>
  .box-card{
    min-height: 260px;
  }
  .box-card i{
    line-height: 160px;
  }
</style>
