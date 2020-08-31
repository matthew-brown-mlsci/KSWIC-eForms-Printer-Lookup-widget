import React from 'react';
import ReactDOM from "react-dom";
import PropTypes from 'prop-types';

import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

//import './fancy.css';
import UserContext from './UserContext.jsx';
import ChangelogTableDisplay from './ChangelogTableDisplay.jsx';
import HospitalTableDisplay from './HospitalTableDisplay.jsx';
import NewRowModal from './NewRowModal.jsx';

import 'react-app-polyfill/ie11';
//import 'react-app-polyfill/stable'

//import { polyfill } from 'es6-promise'; polyfill();
//import '!style-loader!css-loader?module=false';

import './config';

class TabPanel extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { children, value, index, ...other } = this.props;

    return (
      <Typography
        component="div"
        role="tabpanel"
        hidden={value !== index}
        id={`full-width-tabpanel-${index}`}
        aria-labelledby={`full-width-tab-${index}`}
        {...other}
      >
        {value === index && <Box p={3}>{children}</Box>}
      </Typography>
    );
  }
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `full-width-tab-${index}`,
    'aria-controls': `full-width-tabpanel-${index}`,
  };
}

const useStyles = makeStyles((theme) => ({
  root: {
    // backgroundColor: theme.palette.background.paper,
    'display': "contents",
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '50ch',
    },
  },
  '& > *': {
    margin: theme.spacing(1),
  },
  paper: {
    position: 'absolute',
    width: 400,
    backgroundColor: theme.palette.background.paper,
    border: '2px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  },
  save: {
    backgroundColor: '#13AB0C ',
    color: 'white',
  },
  cancel: {
    backgroundColor: '#FFC300',
    color: 'white',
  },
  delete: {
    backgroundColor: '#C70039',
    color: 'white',
  }

}));

function LandingPage() {
  const classes = useStyles();
  const theme = useTheme();
  const [value, setValue] = React.useState(0);
  const [isLoggedIn, setLoggedIn] = React.useState(0);
  const [access_level, set_access_level] = React.useState("");
  const [userID, setUserID] = React.useState("");
  const [domain, setDomain] = React.useState("");
  const [pchost, setHost] = React.useState("");
  const [hospTable, setHospTable] = React.useState("");
  const [origRows, setOrigRows] = React.useState("");
  const [session_passkey, set_session_passkey] = React.useState('');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleChangeIndex = (index) => {
    setValue(index);
  };

  return (
    <div className={classes.root}>
    <center><b><h1>KSWIC Access eForms Printer/Workstation associations</h1></b></center>
    <br />
    <UserContext isLoggedIn={isLoggedIn} setLoggedIn={setLoggedIn} 
                 access_level={access_level} set_access_level={set_access_level}
                 userID={userID} setUserID={setUserID} 
                 domain={domain} setDomain={setDomain}
                 pchost={pchost} setHost={setHost}
                 session_passkey={session_passkey} set_session_passkey={set_session_passkey}/>
    <br />
    <div>
    <AppBar position="static" color="default">
      <Tabs
        value={value}
        onChange={handleChange}
        indicatorColor="primary"
        textColor="primary"
        variant="fullWidth"
        aria-label="full width tabs example"
      >
        <Tab value={0} label="Workstations and Printers" {...a11yProps(0)} />
        <Tab value={1} label="Change Log" {...a11yProps(1)} />
      </Tabs>
    </AppBar>
      <TabPanel value={value} index={0} dir={theme.direction}>
        <div>
          <NewRowModal hospTable={hospTable} userID={userID} domain={domain} origRows={origRows} setOrigRows={setOrigRows} pchost={pchost}
                       session_passkey={session_passkey}/>
          <HospitalTableDisplay isLoggedIn={isLoggedIn} access_level={access_level} userID={userID} domain={domain} pchost={pchost} 
                                hospTable={hospTable} setHospTable={setHospTable} origRows={origRows} setOrigRows={setOrigRows}
                                session_passkey={session_passkey} set_session_passkey={set_session_passkey}/>
        </div>
      </TabPanel>
      <TabPanel value={value} index={1} dir={theme.direction}>
      <div>
        <ChangelogTableDisplay isLoggedIn={isLoggedIn} access_level={access_level} 
                               session_passkey={session_passkey} userID={userID} domain={domain} />
      </div>
      
      </TabPanel>
    
    </div>
  </div>
  );
}


ReactDOM.render(
  <LandingPage />,
  document.getElementById("root")
);