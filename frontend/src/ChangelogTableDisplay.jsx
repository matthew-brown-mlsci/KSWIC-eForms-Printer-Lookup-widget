import React from 'react';

//import "react-tabulator/lib/styles.css"; // default theme
//import "react-tabulator/css/bootstrap/tabulator_bootstrap.min.css"; // use Theme(s)
import { ReactTabulator, reactFormatter } from "react-tabulator"; // for React 15.x

import 'react-app-polyfill/ie11'

class ChangelogTableDisplay extends React.Component {
  constructor(props) {
    super(props);
  }
 
  render() {
    //console.info(this.props);
    return (
      <div>{this.props.isLoggedIn ? <ChangelogTabulator session_passkey={this.props.session_passkey} 
                                                        userID={this.props.userID} 
                                                        domain={this.props.domain} /> : "Changelog is only available after user authorization"} </div>
    );
  }
}

class ChangelogTabulator extends React.Component {
    constructor(props) {
      super(props);
      var self = this;
      //console.info(this);
      this.state = {
        columns: [
          { title: "Created", field: "created", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false },
          { title: "Created by", field: "createdby", width: 90, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false},
          { title: "Log Entry", field: "log_entry", width: 120, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false },
          { title: "New PC ID", field: "new_pc_id", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false },
          { title: "Old PC ID", field: "old_pc_id", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false },
          { title: "New Printer", field: "new_printer", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false },
          { title: "Old Printer", field: "old_printer", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false },
          { title: "Notes", field:"notes", hozAlign:"left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false},
          { title: "Created by host", field:"createdby_host", hozAlign:"left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false},
          { title: "Domain", field:"domain", hozAlign:"left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false},
          { title: "Environment", field:"environment", hozAlign:"left", headerFilter:"input", headerFilterPlaceholder:" ", headerSort:false},
        ],
        original_rows: {},
        options: {
          height: (window.innerHeight - 350).toString() + "px",
          movableRows: false,
          tooltips:true,
          selectable:false,
          dataLoaded:function(data){
            //console.info("dataLoaded");
            //console.info(data);
          },
          rowFormatter:function(row){
              var data = row.getData();
              //console.info(row);
          },
          //setData:function() {this.setState({ data });},
          ajaxProgressiveLoad: 'scroll',
          ajaxFiltering: true,
          ajaxProgressiveLoadDelay: 200,
          ajaxProgressiveLoadScrollMargin: 100,
          ajaxParams: {
                        samAccountName: self.props.userID,
                        domain: self.props.domain,
                        passkey: self.props.session_passkey
                      },
          ajaxURL: global.config.conf.api_endpoint + 'selectChangelogRows',
          cellClick:function(e, cell){ //trigger an alert message when the row is clicked
            //console.info(e);
            //console.info(cell);
            
            },
          ajaxRequestFunc: function(url, config, params) {
            //console.log('Made it to ajaxRequestFunc');
            //console.log('url, config, params');
            //console.info(url);
            //console.info(config);
            //console.info(params);
  
            return new Promise(function(resolve, reject){
              $.ajax({
                url: url,
                data: params,
                type: "GET",  
                dataType: "jsonp",
                timeout: 15000,
                success: function(data) {
                  if (data.success === true) {
                    //console.info(data);
                    self.state.original_rows = JSON.parse(JSON.stringify(data.data));
                    resolve(data);
                  }
                  else {
                    reject();
                  }
                  },
                error: function(jqXHR, textStatus, errorThrown) {
                  reject();
                }
              });
            });
          },
          current_page: 1,
          paginationSize: 50,
          ajaxResponse: function(url, params, response) {
            //console.log('ajaxResponse', url);
            return response; //return the response data to tabulator
          },
          ajaxError: function(error) {
            //console.log('ajaxError', error);
          }
        }
      };
  
    }
  
    render() {
      return (
        <div>
          <ReactTabulator
                ref={ref => (this.ref = ref)}
                columns={this.state.columns}
                data={[]}
                //height={(window.innerHeight - 370).toString() + "px"}
                //rowClick={this.rowClick}
                options={this.state.options}
                data-custom-attr="test-custom-attribute"
                className="custom-css-class"
              />
        </div>
      );
    }
  }

export default ChangelogTableDisplay;