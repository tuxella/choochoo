import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import {Analysis, Diary, Upload, Welcome} from "./pages";
import {Edit, Snapshot, Statistics} from "./pages/kit";
import {Initial, Import, Constants} from "./pages/configure";


export default function Routes() {

    return (
        <BrowserRouter>
            <Switch>
                <Route path='/' exact={true} component={Welcome}/>
                <Route path='/analysis' exact={true} component={Analysis}/>
                <Route path='/configure/initial' exact={true} component={Initial}/>
                <Route path='/configure/import' exact={true} component={Import}/>
                <Route path='/configure/constants' exact={true} component={Constants}/>
                <Route path='/upload' exact={true} component={Upload}/>
                <Route path='/kit/edit' exact={true} component={Edit}/>
                <Route path='/kit/statistics' exact={true} component={Statistics}/>
                <Route path='/kit/:date' exact={true} component={Snapshot}/>
                <Route path='/:date' exact={true} component={Diary}/>
            </Switch>
        </BrowserRouter>
    );
}
