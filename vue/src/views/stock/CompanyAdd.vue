<template>
  <div>
    <a-form
      id="components-form-normal-cu "
      :form="form"
      @submit="handleSubmit"

    >

      <row>
       <a-col span="12">
      <a-form-item v-bind="formItemLayout" label="股票名称:">
        <a-input
          v-decorator="[
            'stockname',
            {
              rules: [{ required: true, message: '请输入要添加股票名称!' }],
            },
          ]"
          style="width: 100%"
        >
        </a-input>
      </a-form-item>
      </a-col>

       <a-col span="12">
      <a-form-item v-bind="formItemLayout" label="交易所:" has-feedback>
        <a-input
          v-decorator="[
            'jys',
            {
              rules: [
                {
                  required: true,
                  message: '请输入要添加的交易所!',
                },

              ],
            },
          ]"

        />
      </a-form-item>
         </a-col>



      </row>





<row>
  <a-col span="8">
    <a-form-item v-bind="formItemLayout" label="公司名称:" has-feedback>
        <a-input
          v-decorator="[
            'name',
            {
              rules: [
                {
                  required: true,
                  message: '请输入要添加的公司名称!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
   <a-col span="8">
 <a-form-item v-bind="formItemLayout" label="公司英文名称:" has-feedback>
        <a-input
          v-decorator="[
            'ename',
            {
              rules: [
                {
                  required: true,
                  message: '请输入要添加的公司英文名称!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
 <a-col span="8">
 <a-form-item v-bind="formItemLayout" label="上市市场:" has-feedback>
        <a-input
          v-decorator="[
            'market',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的上市市场!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
</row>




<row>
  <a-col span="8">
 <a-form-item v-bind="formItemLayout" label="概念及模块:" has-feedback>
        <a-input
          v-decorator="[
            'idea',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的概念及模块!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
<a-col span="8">
 <a-form-item v-bind="formItemLayout" label="上市日期:" has-feedback>
        <a-input
          v-decorator="[
            'ldate',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的上市日期!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
<a-col span="8">
 <a-form-item v-bind="formItemLayout" label="发行价格:" has-feedback>
        <a-input
          v-decorator="[
            'sprice',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的发行价格!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
</row>



<row>
    <a-col span="8">
       <a-form-item v-bind="formItemLayout" label="主承商:" has-feedback>
        <a-input
          v-decorator="[
            'principal',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的主承商!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
      </a-col>
  <a-col span="8">
      <a-form-item v-bind="formItemLayout" label="成立日期:" has-feedback>
        <a-input
          v-decorator="[
            'rdate',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的成立日期!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
    </a-col>
  <a-col span="8">
           <a-form-item v-bind="formItemLayout" label="注册成本:" has-feedback>
        <a-input
          v-decorator="[
            'rprice',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的注册成本!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
    </a-col>
</row>


<row>
   <a-col span="8">
        <a-form-item v-bind="formItemLayout" label="机构类型:" has-feedback>
        <a-input
          v-decorator="[
            'instype',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的机构类型!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
      <a-col span="8">
  <a-form-item v-bind="formItemLayout" label="组织形式:" has-feedback>
        <a-input
          v-decorator="[
            'organ',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的组织形式!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
 <a-col span="8">
  <a-form-item v-bind="formItemLayout" label="公司电话:" has-feedback>
        <a-input
          v-decorator="[
            'phone',
            {
              rules: [
                {
                  required:false,
                  message: '请输入要添加的公司电话!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
</row>



<row>
  <a-col span="8">
<a-form-item v-bind="formItemLayout" label="公司网站:" has-feedback>
        <a-input
          v-decorator="[
            'site',
            {
              rules: [
                {
                  required: false,
                  message: '请输入修改的公司网站!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
<a-col span="8">
<a-form-item v-bind="formItemLayout" label="公司邮编:" has-feedback>
        <a-input
          v-decorator="[
            'post',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的公司邮编!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
</a-col>
<a-col span="8">
<a-form-item v-bind="formItemLayout" label="注册地址:" has-feedback>
        <a-input

          v-decorator="[
            'addr',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的注册地址!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
  </a-col>
</row>



<row>
  <a-col span="12">
<a-form-item v-bind="formItemLayout" label="办公地址:" has-feedback>
        <a-input
          v-decorator="[
            'oddr',
            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的办公地址!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
      </a-col>
<a-col span="12">
<a-form-item v-bind="formItemLayout" label="公司简介:" has-feedback  >
        <a-input
          v-decorator="[
            'desc',

            {
              rules: [
                {
                  required: false,
                  message: '请输入要添加的公司简介!',
                },
              ],
            },
          ]"
        />
      </a-form-item>
    </a-col>
</row>



<!--      ###############################################-->
    <row>
      <a-col span="16">
 <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          size="large"
          class="register-form-button"
          :loading="loading"
           style="  width: 400px;float: right"
        >
          添加
        </a-button>
      </a-form-item>

<a-form-item >
        <a-button
          type="danger"
          html-type="reset"
          size="large"
          class="register-form-button"
          :loading="loading"
          style="  width: 400px;float: right"
        >
          重置
        </a-button>
      </a-form-item>

      <a-form-item>
        <div style="float: right;font-size: 20px" >
         <a @click="to_user_manage"> 返回 </a>
        </div>
      </a-form-item>

      </a-col>
</row>

    </a-form>



  </div>
</template>


<script>


export default {
  name: "CompanyAdd",
  data() {
    return {
      loading: false,
      confirmDirty: false,

      formItemLayout: {
        labelCol: {
          // xs: { span: 16 },
          xs: { span: 10   },
          // sm: { span: 4 },
          sm: { span: 5 },
        },
        wrapperCol: {
          // xs: { span: 24 },
          xs: { span: 24 },
          // sm: { span: 20 },
          sm: { span: 15 },
        },
      },
    };
  },


  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "update" });
  },

  methods: {
    /**
     * 提交表格数据
     */
    handleSubmit(e) {
      this.loading = true
      e.preventDefault();
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          let data = {
            stockname: values["stockname"],
            jys: values["jys"],
            name: values["name"],
            ename: values["ename"],
            market: values["market"],
            idea: values["idea"],
            ldate: values["ldate"],
            sprice: values["sprice"],
            principal: values["principal"],
            rdate: values["rdate"],
            rprice: values["rprice"],
            instype: values["instype"],
            organ:values["organ"],
            phone: values["phone"],
            site: values["site"],
            post: values["post"],
            addr: values["addr"],
            oaddr: values["oaddr"],
            desc: values["desc"],
          };
          console.log("Received values of form: ", data);
          this.$stock_api.add_company(data).then((res) => {
            // 请求后端数据
            if (res.code==200) {
              this.$message.success(" 添加成功！");
              this.$router.push({
                path: `/company-manage`,
              });
            } else {
              this.$message.error(res.msg);
            }
            this.loading = false
          }).catch(() => {
            this.$message.error('连接到服务器失败')
            this.loading = false
          })
        } else {
          this.loading = false
        }

      });
    },



    // 跳转登录页面
    to_user_manage() {
      this.$router.push({
        path: `/company-manage`,
      });
    },


  },
};
</script>

<style scoped>
#components-form-normal-cu {
  min-width: 450px;
  width: 600px;
  margin: 5rem auto;
}

#components-form-normal-cu .register-form-button {
  width: 100%;
}
</style>