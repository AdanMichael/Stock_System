<template>
  <div>
    <a-row type="flex">
    <a-col flex="40%" style="margin-left:5rem;">
        <!-- 搜索自选股对话框 -->
        <div>
          <span>股票名称：</span>
          <a-auto-complete
            v-model="input"
            style="width: 50%"
            placeholder="请输入"
            @search="onSearchUser"
          /><a-spin :spinning="searchLoading"/>
          </div>
      </a-col>

    <a-col flex="auto">
        <a-button type="primary" @click="btnSearchUser">
          搜索
        </a-button>
      </a-col>
    <a-col flex="auto">
       <a-button type="primary" @click="refresh">
         更新数据
        </a-button>
    </a-col>



       </a-row>
   <!-- 表格数据展示 -->
    <a-table
      :columns="columns"
      :data-source="data"
      :pagination="pagination"
      :loading="loading"
      @change="handleTableChange"
      style="margin-top:2rem;"
    >
      <!-- 购入详情页面 -->
      <template slot="index" slot-scope="text">
        {{ text }}
      </template>
      <template slot="dm" slot-scope="text, row">
        {{ text }}
      </template>
      <template slot="mc" slot-scope="text, row">
        {{ text }}
      </template>
      <template slot="num" slot-scope="text">
        {{ text }}
      </template>
      <template slot="bp" slot-scope="text">
       {{ text }}
      </template>
      <template slot="bt" slot-scope="text">
       {{ text }}
      </template>
      <template slot="p" slot-scope="text">
        {{ text }}
      </template>

      <!-- 删除 -->
      <template slot="operation" slot-scope="text, row">

        <a-button
          type="danger"
          @click="sell(row.index,row.dm)"
          style="margin-right: 2rem"
          >抛出</a-button
        >

<!--        <a-button type="primary" @click="cal_profit(row.index,row.dm)">-->
<!--        <a-button type="primary" @click="cal_profit()">-->
<!--         更新-->
<!--        </a-button>-->


      </template>
    </a-table>


  </div>
</template>



<script >
import Footer from "@/components/Footer.vue";
import RealBlcok from "@/components/RealBlock.vue";

// 表格表头
const columns = [
  {
    title: "Index",
    dataIndex: "index",
    key: 'index',
    width: "10%",
  },
    {
    title: "股票代码",
    dataIndex: "dm",
    key: 'dm',
    width: "10%",
    scopedSlots: { customRender: "dm" },
  },

  {
    title: "股票名称",
    dataIndex: "mc",
    key: 'mc',
    width: "10%",
    scopedSlots: { customRender: "mc" },
  },
  {
    title: "买入数量(单位：股)",
    dataIndex: "num",
    key: 'num',
    width: "10%",
    scopedSlots: { customRender: "num" },
  },
  {
    title: "买入价格(单位：股)",
    dataIndex: "bp",
    key: 'bp',
    width: "10%",
    scopedSlots: { customRender: "bp" },
  },

  {
    title: "买入时间",
    dataIndex: "bt",
    key: 'bt',
    width: "15%",
    scopedSlots: { customRender: "bt" },
  },

  {
    title: "收益",
    dataIndex: "p",
    key: 'p',
    width: "10%",
    scopedSlots: { customRender: "p" },
  },

      {
    title: "操作",
    dataIndex: "operation",
    key: 'operation',
    width: "10%",
    scopedSlots: { customRender: "operation" },
  },


];


export default {
  name: "MyStock",
  props: {
    user_info: {
      type: Object,
    },
  },
  components: {
    Footer
  },
  data() {
    return {
      loading: false,
      searchLoading: false,
      data: [],
      columns,
      pagination: {
        pageSize: 5,
        current: 1,
      },
      dataSource: [], // 搜索框数据源
      input: "",
      userId: this.user_info.id,
      real_data: {},
      Index:[],  //这是js，不是python,所以是数组不是列表
      Code:[]  //这是js，不是python,所以是数组不是列表
    };
  },
  mounted() {
    this.get_stocks()
  },

  methods: {
 /**
     * 处理表格分页
     */
    handleTableChange(pagination) {
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.get_stocks()
    },


    // ==================
    // 股票名称搜索框
    // ==================
    onSearchUser(searchText) {
      this.input = searchText;
    },
    /**
     * 点击搜索按钮
     */
    btnSearchUser() {
      // this.value_code = null
       if (this.input.trim().length==0){
          this.get_stocks();
        }

       else {
         this.get_stock();
       }
    },


    /**
     * 搜索框数据源获取
     */
    get_stocks() {
      let param = {
        account_id:this.userId,
      }
      this.$alipay_api.get_stocks(param).then((res) => {
        this.loading = true
        let dataSource = [];
        if (res.code == 200) {
          console.log(res);
             for (let i = 0; i < res.data.stocks.length; i++) {
              dataSource.push(
                  {
                    'index': res.data.stocks[i]["index"],
                    'dm': res.data.stocks[i]["code_id"],
                    'mc': res.data.stocks[i]['stockname'],
                    'num': res.data.stocks[i]['stocknum'],
                    'bt': res.data.stocks[i]['buy_time'],
                    'bp': res.data.stocks[i]['buy_price'],
                    'p':this.formatProfit( res.data.stocks[i]['pofit'])
                  }
              );
            }
          this.data = dataSource
          // 分页处理
          const pagination = { ...this.pagination };
          pagination.total = res.data.sum;
          this.pagination = pagination;
          this.loading = false
        }
      });
    },


    get_stock() {
      let param={
        account_id:this.userId,
        search:this.input,
      }
        this.$alipay_api.get_stock(param).then((res) => {
          this.loading = true
          let dataSource = [];
          if (res.code == 200) {
            console.log(res);
            for (let i = 0; i < res.data.stocks.length; i++) {
              dataSource.push(
                {
                    'index': res.data.stocks[i]["index"],
                    'dm': res.data.stocks[i]["code_id"],
                    'mc': res.data.stocks[i]['stockname'],
                    'num': res.data.stocks[i]['stocknum'],
                    'bp': res.data.stocks[i]['buy_price'],
                    'bt': res.data.stocks[i]['buy_time'],
                    'p':this.formatProfit( res.data.stocks[i]['pofit'])
                  }
              );
            }
            this.data = dataSource
            // 分页处理
            const pagination = {...this.pagination};
            pagination.total = res.data.sum;
            this.pagination = pagination;
            this.loading = false
          }
         });
    },


  formatProfit(profit) {
          if (profit == undefined) {
              return 0
          }
          return profit
      },

  //抛出
    sell(index,code){
    let r=confirm("确定抛出吗？");
			if (r==true){
        this.$stock_api.get_stock_day(code).then((res) => {
          if (res.code===200){
          this.real_data = res.data
                let param={
                 uid:this.user_info.id,
                 index:index,
                 sell_price:this.real_data.p,
                }
                console.log(param.sell_price)
              this.$alipay_api.sell(param).then((res) => {
                if (res) {
                  window.alert("已抛出")
                  this.$router.go(0)
                }
              })
          }
        })
      }
      else{
        window.alert("已取消")
			  }

    },






     //刷新股票实时数据
        refresh() {
            // 遍历data数组
          this.data.forEach(item => {
            // 遍历columns数组中的每个列对象
            this.columns.forEach(column => {
              // 检查每个列对象是否有dataIndex属性，并且dataIndex等于"dm"
              if (column.dataIndex === 'index') {
                // 输出股票代码属性列的值
                this.Index.push(item[column.dataIndex])
              }
              if (column.dataIndex === 'dm') {
                // 输出股票代码属性列的值
                this.Code.push(item[column.dataIndex])
              }
            });
          });

          for (let i = 0; i <this.Index.length; i++) {
            this.$stock_api.get_stock_day(this.Code[i]).then((res) => {
                if (res.code === 200) {
                     this.real_data = res.data
                     let param={
                     index:this.Index[i],
                     price:this.real_data.p,
                    }
                  this.$alipay_api.update_profit(param).then((res) => {
                     if (res){console.log("ok")}
                  })

                } else {
                    this.$message.error('请求过于频繁,请2秒后刷新页面,重新进行请求!');
                }
            })
            }
          window.alert("已更新")
          this.$router.go(0)
        },





    },
};
</script>
