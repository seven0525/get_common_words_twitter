import React, { Component }from 'react';

import Layout from '../components/Layout';

import { BarChart,XAxis, YAxis, Bar } from 'recharts';

import { StaggeredMotion, spring, Motion } from 'react-motion';

import APP from '../components/APP';
import Nodes from '../components/Nodes';
import Nodes1 from '../components/Nodes1';

import LineTo from 'react-lineto';



import { ParentSize } from '@vx/responsive'


import Tree from '../components/tree/Tree'
import data from '../components/tree/data'
import APPfirst from "../components/APPfirst";

class Result extends Component {

    state={
        most_used_keyword: '',
        second_keyword:'',
        third_keyword:'',
        fourth_keyword:'',
        fifth_keyword:'',
        sixth_keyword:'',
        seventh_keyword:'',
        eighth_keyword:'',
        ninth_keyword:'',
        array_results:'',
        line:''
    }

    componentDidMount(){

        var json_results = sessionStorage.getItem('json_results');

        //key_tweetsをjson?からとってくる
        //setStateでセットする
        //それぞれの内リストで全部分けて変数に格納する
        //変数をこのページで表示する

        // bracketを除去する

        var str_results = json_results.replace(/\s|\[|\]|\"/g, "" ) ;

        var array_results =  str_results.split(',');

        this.setState({most_used_keyword: array_results[0],
            second_keyword:array_results[2],
            third_keyword:array_results[4],
            fourth_keyword:array_results[6],
            fifth_keyword:array_results[8],
            sixth_keyword:array_results[10],
            seventh_keyword:array_results[12],
            eighth_keyword:array_results[14],
            ninth_keyword:array_results[16],
            array_results: array_results,
            line:<LineTo borderWidth={3} borderColor="red" from="main-button" to="child-button" />


        })





    }

    render(){

        const data_array_results = this.state.array_results

        console.log(this.state.line)


        const data = [
            { name: data_array_results[0] ,  pv: data_array_results[1] , number:100},
            { name: data_array_results[2],  pv: data_array_results[3] },
            { name: data_array_results[4],  pv: data_array_results[5] },
            { name: data_array_results[6],  pv: data_array_results[7] },
            { name: data_array_results[8],  pv: data_array_results[9] },
            { name: data_array_results[10], pv: data_array_results[11] }
        ]

        return(
            <Layout>
            <div>
                <div style={{backgroundColor:"#FFFFFF",
                   marginTop: "50px", height:"300px"
                }}>
                    <div style={{color:"#000000",
                        float:'left',
                        marginLeft:"180px",
                        marginTop:"50px"
                    }}>

                    <h4 >最頻キーワード</h4>

                    <h1 style={{marginTop: "70px"}}>{this.state.most_used_keyword}</h1>
                    </div>

                    <div style={{color:"#000000",  float:"right",
                        marginRight:"200px",
                        marginTop:"50px"
                    }}>

                    <h4 >予測精度</h4>

                        <h1　style={{marginTop: "70px"}}>65.5%</h1>


                    </div>

                </div>

                <div style={{backgroundColor:"#FFFFFF",
                    marginTop: "50px", height:"300px"

                }}>
                    <h2 style={{color:"#000000"}}>keyword graph</h2>

                    <BarChart
                        width={600}
                        height={300}
                        layout="vertical"
                        margin={{top: 5, right: 30, left: 20, bottom: 5}}
                        data={data}
                    >
                        <XAxis type="number" dataKey="number"/>
                        <YAxis type="category" dataKey="name"
                               tick={{fontSize: 20, fontWeight: "bold"}}
                        />

                        <Bar dataKey="pv" fill="#5C9BD5" />
                    </BarChart>

                </div>

                <div style={{backgroundColor:"#FFFFFF",
                    marginTop: "50px",  height:"300px", marginBottom:"50px"

                }}>
                    <h2 style={{color:"#000000"}}>keyword map</h2>

                    <APPfirst keyword={data_array_results[0]} number={data_array_results[1]} space={"0"}/>


                    <APP  keyword={data_array_results[2]} number={data_array_results[3]}

                          count={0}

                          space={data_array_results[1]}/>
                    <APP  keyword={data_array_results[4]} number={data_array_results[5]}
                          count={30}　
                          space={data_array_results[3]}/>

                    <APP  keyword={data_array_results[6]} number={data_array_results[7]}
                          count={60}
                          space={data_array_results[5]}/>

                    <APP  keyword={data_array_results[8]} number={data_array_results[9]}
                          count={90}
                          space={data_array_results[7]}/>

                    <APP  keyword={data_array_results[10]} number={data_array_results[11]}
                          count={110}
                          space={data_array_results[9]}/>

                    <APP  keyword={data_array_results[12]} number={data_array_results[13]}
                          count={130}
                          space={data_array_results[11]}/>

                    <APP  keyword={data_array_results[14]} number={data_array_results[15]}
                          count={150}
                          space={data_array_results[13]}/>

                    <APP  keyword={data_array_results[16]} number={data_array_results[17]}
                          count={170}
                          space={data_array_results[15]}/>


                </div>
            </div>
            </Layout>
        )
    }





}

export default Result;