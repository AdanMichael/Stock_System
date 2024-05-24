<template>
  <div>
    <a-form
      id="components-form-normal-register"
      :form="form"
      @submit="handleSubmit"
    >
      <a-form-item v-bind="formItemLayout" label="手机号">
        <a-input
          v-decorator="[
            'phone',
            {
              rules: [{ required: true, message: '请输入修改的手机号!' }],
            },
          ]"
          style="width: 100%"
        >
          <a-select
            slot="addonBefore"
            v-decorator="['prefix', { initialValue: '86' }]"
            style="width: 70px"
          >
            <a-select-option value="86"> +86 </a-select-option>
            <a-select-option value="87"> +87 </a-select-option>
          </a-select>
        </a-input>
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="新密码" has-feedback>
        <a-input
          v-decorator="[
            'password',
            {
              rules: [
                {
                  required: true,
                  message: '请输入长度大于5的新密码!',
                },
                {
                  validator: validateToNextPassword,
                },
              ],
            },
          ]"
          type="password"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="确认新密码" has-feedback>
        <a-input
          v-decorator="[
            'confirm',
            {
              rules: [
                {
                  required: true,
                  message: '请再次输入新密码!',
                },
                {
                  validator: compareToFirstPassword,
                },
              ],
            },
          ]"
          type="password"
          @blur="handleConfirmBlur"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout">
        <span slot="label">
          昵称&nbsp;

        </span>
        <a-input
          v-decorator="[
            'nickname',
            {
              rules: [
                {
                  required: true,
                  message: '请输入修改的昵称!',
                  whitespace: true,
                },
              ],
            },
          ]"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout">
        <span slot="label">
          用户资产&nbsp;
        </span>
        <a-input
          v-decorator="[
            'rest_asset',
            {
              rules: [
                {
                  required: false,
                  message: '请输入修改的用户资产!',
                  whitespace: true,
                },
              ],
            },
          ]"
        />
      </a-form-item>

    <a-form-item v-bind="formItemLayout">
        <span slot="label">
          盈亏资产
        </span>
        <a-input
          v-decorator="[
            'profit_asset',
            {
              rules: [
                {
                  required: false,
                  message: '请输入修改的盈亏资产!',
                  whitespace: true,
                },
              ],
            },
          ]"
        />
      </a-form-item>


      <a-form-item>
        <div style="float: right">
         <a @click="to_user_manage"> 返回 </a>
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
  name: "UserUpdate",
  data() {
    return {
      loading: false,
      confirmDirty: false,
      id: this.$route.query.id,
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
            id:this.id,
            phone: values["phone"],
            password: values["password"],
            nickname: values["nickname"],
            rest_asset: values["rest_asset"],
            profit_asset: values["profit_asset"],
          };
          console.log("Received values of form: ", data);
          this.$user_api.update(data).then((res) => {
            // 请求后端数据
            if (res) {
              this.$message.success("修改成功！");
              this.$router.push({
                path: `/user-manage`,
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
    // 处理输入框数据
    handleConfirmBlur(e) {
      const value = e.target.value;
      this.confirmDirty = this.confirmDirty || !!value;
    },
    // 核实两次密码是否一致
    compareToFirstPassword(rule, value, callback) {
      const form = this.form;
      if (value && value !== form.getFieldValue("password")) {
        callback("两次密码输入不一致!");
      } else {
        callback();
      }
    },
    validateToNextPassword(rule, value, callback) {
      const form = this.form;
      if (value && this.confirmDirty) {
        form.validateFields(["confirm"], { force: true });
      }
      callback();
    },
    // 跳转登录页面
    to_user_manage() {
      this.$router.push({
        path: `/user-manage`,
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