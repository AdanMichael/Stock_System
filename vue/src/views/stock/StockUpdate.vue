<template>
  <div>
    <a-form
      id="components-form-normal-register"
      :form="form"
      @submit="handleSubmit"
    >
      <a-form-item v-bind="formItemLayout" label="购入数量">
        <a-input
          v-decorator="[
            'stocknum',
            {
              rules: [{ required: true, message: '请输入要修改的购入数量!' }],
            },
          ]"
          style="width: 100%"
        >
        </a-input>
      </a-form-item>

      <a-form-item v-bind="formItemLayout" label="买入价格">
        <a-input
          v-decorator="[
            'buy_price',
            {
              rules: [{ required: true, message: '请输入要修改的买入价格!' }],
            },
          ]"
          style="width: 100%"
        >
        </a-input>
      </a-form-item>

        <a-form-item v-bind="formItemLayout" label="盈利">
        <a-input
          v-decorator="[
            'profit',
            {
              rules: [{ required: true, message: '请输入要修改的盈利!' }],
            },
          ]"
          style="width: 100%"
        >
        </a-input>
      </a-form-item>



      <a-form-item>
        <div style="float: right">
          <a @click="to_login"> 返回 </a>
        </div>
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          size="large"
          class="register-form-button"
          :loading="loading"
        >
          修改
        </a-button>
      </a-form-item>
    </a-form>
  </div>

</template>

<script>
export default {
  name: "StockUpdate",
  data() {
    return {
      index: this.$route.query.index,
      loading: false,
      confirmDirty: false,
      formItemLayout: {
        labelCol: {
          xs: { span: 16 },
          sm: { span: 4 },
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 20 },
        },
      },
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "StockUpdate" });
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
            index:this.index,
            stocknum: values["stocknum"],
            buy_price: values["buy_price"],
            profit: values["profit"],
          };
          console.log("Received values of form: ", data);
          this.$alipay_api.update_stock(data).then((res) => {
            // 请求后端数据
            if (res) {
              this.$message.success("修改成功！");
              this.$router.push({
                path: `/user-money`,
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
    to_login() {
      this.$router.push({
        path: `/user-money`,
      });
    },
  },
};
</script>

<style scoped>
#components-form-normal-register {
  min-width: 450px;
  width: 600px;
  margin: 5rem auto;
}

#components-form-normal-register .register-form-button {
  width: 100%;
}
</style>