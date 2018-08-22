import React, { Component }from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';
import { Input, Form, Modal, Header, Loader, Dimmer } from 'semantic-ui-react';
import axios from 'axios';
import APP from '../components/APP';
import { ClipLoader, BeatLoader } from 'react-spinners';
import ReactSVG from 'react-svg';
import { FaSearch } from 'react-icons/fa';




class Index extends Component{

    state={
        keyword:'',
        results:'',
        key_tweets:'',
        modalOpen:false
    }

    onSubmit(){

        this.setState({modalOpen:true})


        //results/Key_tweetsを取得してjsonに格納
        axios
            .get("http://localhost:3001/result", { params: {keyword: this.state.keyword}　})
            .then((results, key_tweets) => {
                // 通信に成功してレスポンスが返ってきた時に実行したい処理
                console.log(results, key_tweets)
                this.setState({results: results.data})
                this.setState({key_tweets: key_tweets})

                var json_results = JSON.stringify(results.data)
                var json_key_tweets = JSON.stringify(key_tweets)

                sessionStorage.setItem('json_results', json_results);
                sessionStorage.setItem('json_key_tweets', json_key_tweets);

                location.href = "http://localhost:3000/result" ;



            })




    }






    render(){

        console.log(this.state.results)


        return(
            <Layout>

            <div>

                <h1　style={{color:"#FFFFFF", fontSize:"50px",
                    marginRight:'35px',
                    marginLeft: "300px", paddingTop:"200px"}}>
                    潜在需要を見つけよう
                </h1>

                <Form onSubmit={this.onSubmit.bind(this)}>


                <Input placeholder='キーワードを入力'
                       style={{background: 'rgba(255,255,255,0.8)', width: "300px",
                           height:"50px", placeholder:'100px',
                           marginLeft:"370px", fontSize:"30px",color:"#ffffff"
                       }}
                       transparent = "true"
                       value={this.state.keyword}
                       onChange={event =>
                           this.setState({ keyword: event.target.value})}


                />

                    <i>

                    <FaSearch />

                    </i>


                </Form>

                <Modal open={this.state.modalOpen}>
                    <Modal.Content>
                        <Modal.Description>
                            <p　style={{color:"#000000", float:"left", fontSize:"20px"}}>
                                tweetを解析しております 少々お待ちください   </p>
                            {/*<Dimmer active inverted>*/}
                            <BeatLoader
                                sizeUnit={"px"}
                                size={20}
                                color={'#123abc'}
                                loading="true"

                            />

                            {/*</Dimmer>*/}
                        </Modal.Description>
                    </Modal.Content>
                </Modal>

            </div>

            </Layout>

        )
    }



}

export default Index;