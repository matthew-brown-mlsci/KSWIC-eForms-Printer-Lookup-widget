import React from 'react';

import 'react-app-polyfill/ie11'

import './config';

class UserContext extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        user_txt: "",
        domain_txt: "",
        host_txt:"",
        session_passkey:"",
        access_from_user_or_group: "",
        access_level: "Access NOT granted",
        ad_resource: "None found",
        cached_access: false,    
      };
    }
  
    componentDidMount() {
      var self = this;
      //console.info('componentDidMount');
      //console.info(props);
      
      var target_url = global.config.conf.api_endpoint + 'getWinAuthInfo';
      $.ajax({
        url: target_url,
        type: "GET",  
        dataType: "jsonp",
        timeout: 15000,
        success: function(data) {
          if (data.success === true) {
            //console.info(data);
            //console.info(self);
            self.setState({user_txt: data.user_txt,
                           domain_txt: data.domain_txt,
                           host_txt: data.host_txt});
            self.props.setDomain(data.domain_txt);
            self.props.setUserID(data.user_txt);
            self.props.setHost(data.host_txt);
          }
          else {
            self.setState({user_txt: "unknown",
              domain_txt: "unknown",
              host_txt: "unknown"});
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {
          self.setState({user_txt: ('Cannot contact KSWIC Printer_Lookup API: ' + target_url),
              domain_txt: "unknown",
              host_txt: "unknown"});
            }
      }).then(function(promise_data){
        //console.info('made it to then() clause for verifyUserAccess');
        //console.info(promise_data);
        var target_url = global.config.conf.api_endpoint + 'verifyUserAccess';
        var url_args = {domain: self.state.domain_txt,
                    samAccountName: self.state.user_txt
        }
        $.ajax({
          url: target_url,
          data: url_args,
          type: "GET",  
          dataType: "jsonp",
          timeout: 15000,
          success: function(data) {
            if (data.success === true) {
              //console.info(data);
              //console.info(self);
              self.setState({session_passkey: data.passkey,
                             access_from_user_or_group: data.access_from_user_or_group,
                             access_level: data.access_level,
                             ad_resource: data.ad_resource,
                             cached_access: data.cached_access});
              
              self.props.set_session_passkey(data.passkey);
              self.props.set_access_level(data.access_level);
              self.props.setLoggedIn(true);
              //console.info('self.props.session_passkey');
              //console.info(self.props.session_passkey);
              
            }
            else {
                self.setState({user_txt: "unknown",
                domain_txt: "unknown",
                host_txt: "unknown"});
            }
          },
          error: function(jqXHR, textStatus, errorThrown) {
            self.setState({user_txt: ('Cannot contact KSWIC Printer_Lookup API: ' + target_url),
                            domain_txt: "unknown",
                            host_txt: "unknown"});
                          }
        });
      });
    }
  
    render() {
      return (
        <div>
          <h4>Logged in as:</h4>
          <div style={{float: "left"}}>User ID: {this.state.user_txt}</div><div style={{float: "right"}}>Access Level: <b>{this.state.access_level}</b></div>
          <br />
          <div style={{float: "left"}}>Domain: {this.state.domain_txt}</div><div style={{float: "right"}}>AD Resource granting access: {this.state.ad_resource}</div>
          <br />
          <div style={{float: "left"}}>PC Hostname: {this.state.host_txt}</div><div style={{float: "right"}}>Cached access: {this.state.cached_access ? 'True' : 'False'}</div>
          <br />
  
        </div>
      );
    }
  }

  export default UserContext;