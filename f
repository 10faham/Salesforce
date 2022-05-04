            
                                                    <div class="tab-pane" id="today">
                                                        <div class="card-box table-responsive">
                        
                                                            <table id="datatable-buttons" class="table table-striped table-bordered">
                                                                <thead>
                                                                    <tr>
                                                                        <th>#</th>
                                                                        <th>Task</th>
                                                                        <th>Deadline</th>
                                                                        <th>Client</th>
                                                                        <th>Project</th>
                                                                        <th>Comment</th>
                                                                        <th>Assigned To</th>
                                                                        <th>Actions</th>
                                                                    </tr>
                                                                </thead>
                        
                        
                                                                <tbody id="lead-detail">
                                                                    {% for user in response_data['followup'] %}
                                                                    {% for obj in user[2] %}
                                                                    {% if moment(obj.data.next_deadline).format('YYYY MM DD') == moment().format('YYYY MM DD') %}
                                                                    <tr>
                                                                        <td scope="row">{{loop.index}}<button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="right" title="" data-original-title="'{{obj.data.lead.id}}'"><i class="mdi mdi-key-variant"></i></button></td>
                                                                        <td>{{obj.data.next_task}}</td>
                                                                        <td>{{moment(obj.data.next_deadline).calendar()}}</td>
                                                                        <td>{{obj.data.lead.first_name}}</td>
                                                                        <td>{{obj.data.next_project}}</td>
                                                                        <td>{{obj.data.comment}}</td>
                                                                        <td>{{user[0]}}</td>
                                                                        <td><a href="/api/follow_ups/create?lead={{obj.data.lead.id}}"><i class="glyphicon glyphicon-plus"></i></a>
                                                                            <button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="top" title="" data-original-title="'{{obj.data.lead.phone_number}}'"><i class="mdi mdi-cellphone-basic"></i></button>
                                                                            <form class="" action="/api/follow_ups/follow_read" method="POST" id="follow_up_lead">
                                                                                <input type="hidden" name="lead" value="{{obj.data.lead.id}}" >
                                                                            <input type="submit" class="mdi mdi-file-restore" value="view all">
                                                                            </form>
                                                                        </td>
                                                                    </tr>
                                                                    {% endif %}
                                                                    {% endfor %}
                                                                    {% endfor %}
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                    <div class="tab-pane" id="tomorrow">
                                                        <div class="card-box table-responsive">
                        
                                                            <table id="datatable-buttons" class="table table-striped table-bordered">
                                                                <thead>
                                                                    <tr>
                                                                        <th>#</th>
                                                                        <th>Task</th>
                                                                        <th>Deadline</th>
                                                                        <th>Client</th>
                                                                        <th>Project</th>
                                                                        <th>Comment</th>
                                                                        <th>Assigned To</th>
                                                                        <th>Actions</th>
                                                                    </tr>
                                                                </thead>
                        
                        
                                                                <tbody id="lead-detail">
                                                                    {% for user in response_data['followup'] %}
                                                                    {% for obj in user[2] %}
                                                                    {% if moment(obj.data.next_deadline).format('YYYY MM DD') > moment().format('YYYY MM DD') %}
                                                                    <tr>
                                                                        <th scope="row">{{loop.index}}<button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="right" title="" data-original-title="'{{obj.data.lead.id}}'"><i class="mdi mdi-key-variant"></i></button></th>
                                                                        <td>{{obj.data.next_task}}</td>
                                                                        <td>{{moment(obj.data.next_deadline).calendar()}}</td>
                                                                        <td>{{obj.data.lead.first_name}}</td>
                                                                        <td>{{obj.data.next_project}}</td>
                                                                        <td>{{obj.data.comment}}</td>
                                                                        <td>{{user[0]}}</td>
                                                                        <td><a href="/api/follow_ups/create?lead={{obj.data.lead.id}}"><i class="glyphicon glyphicon-plus"></i></a>
                                                                            <button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="top" title="" data-original-title="'{{obj.data.lead.phone_number}}'"><i class="mdi mdi-cellphone-basic"></i></button>
                                                                            <form class="" action="/api/follow_ups/follow_read" method="POST" id="follow_up_lead">
                                                                                <input type="hidden" name="lead" value="{{obj.data.lead.id}}" >
                                                                            <input type="submit" class="mdi mdi-file-restore" value="view all">
                                                                            </form>
                                                                        </td>
                                                                    </tr>
                                                                    {% endif %}
                                                                    {% endfor %}
                                                                    {% endfor %}
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                    <div class="tab-pane" id="next7day">
                                                        <div class="card-box table-responsive">
                        
                                                            <table id="datatable-buttons" class="table table-striped table-bordered">
                                                                <thead>
                                                                    <tr>
                                                                        <th>#</th>
                                                                        <th>Task</th>
                                                                        <th>Deadline</th>
                                                                        <th>Client</th>
                                                                        <th>Project</th>
                                                                        <th>Comment</th>
                                                                        <th>Assigned To</th>
                                                                        <th>Actions</th>
                                                                    </tr>
                                                                </thead>
                        
                        
                                                                <tbody id="lead-detail">
                                                                    {% for user in response_data['followup'] %}
                                                                    {% for obj in user[2] %}
                                                                    {% if moment(obj.data.next_deadline).format('YYYY MM DD') > moment().format('YYYY MM DD') %}
                                                                    <tr>
                                                                        <th scope="row">{{loop.index}}<button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="right" title="" data-original-title="'{{obj.data.lead.id}}'"><i class="mdi mdi-key-variant"></i></button></th>
                                                                        <td>{{obj.data.next_task}}</td>
                                                                        <td>{{moment(obj.data.next_deadline).calendar()}}</td>
                                                                        <td>{{obj.data.lead.first_name}}</td>
                                                                        <td>{{obj.data.next_project}}</td>
                                                                        <td>{{obj.data.comment}}</td>
                                                                        <td>{{user[0]}}</td>
                                                                        <td><a href="/api/follow_ups/create?lead={{obj.data.lead.id}}"><i class="glyphicon glyphicon-plus"></i></a>
                                                                            <button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="top" title="" data-original-title="'{{obj.data.lead.phone_number}}'"><i class="mdi mdi-cellphone-basic"></i></button>
                                                                            <form class="" action="/api/follow_ups/follow_read" method="POST" id="follow_up_lead">
                                                                                <input type="hidden" name="lead" value="{{obj.data.lead.id}}" >
                                                                            <input type="submit" class="mdi mdi-file-restore" value="view all">
                                                                            </form>
                                                                        </td>
                                                                    </tr>
                                                                    {% endif %}
                                                                    {% endfor %}
                                                                    {% endfor %}
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                    <div class="tab-pane" id="all">
                                                        <div class="card-box table-responsive">
                        
                                                            <table id="datatable-buttons" class="table table-striped table-bordered">
                                                                <thead>
                                                                    <tr>
                                                                        <th>#</th>
                                                                        <th>Task</th>
                                                                        <th>Deadline</th>
                                                                        <th>Client</th>
                                                                        <th>Project</th>
                                                                        <th>Comment</th>
                                                                        <th>Assigned To</th>
                                                                        <th>Actions</th>
                                                                    </tr>
                                                                </thead>
                        
                        
                                                                <tbody id="lead-detail">
                                                                    {% for user in response_data['followup'] %}
                                                                    {% for obj in user[2] %}
                                                                    <tr>
                                                                        <th scope="row">{{loop.index}}<button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="right" title="" data-original-title="'{{obj.data.lead.id}}'"><i class="mdi mdi-key-variant"></i></button></th>
                                                                        <td>{{obj.data.next_task}}</td>
                                                                        <td>{{moment(obj.data.next_deadline).calendar()}}</td>
                                                                        <td>{{obj.data.lead.first_name}}</td>
                                                                        <td>{{obj.data.next_project}}</td>
                                                                        <td>{{obj.data.comment}}</td>
                                                                        <td>{{user[0]}}</td>
                                                                        <td><a href="/api/follow_ups/create?lead={{obj.data.lead.id}}"><i class="glyphicon glyphicon-plus"></i></a>
                                                                            <button type="button" class="btn btn-default" style="border: none; padding: 0px 4px" data-toggle="tooltip" data-placement="top" title="" data-original-title="'{{obj.data.lead.phone_number}}'"><i class="mdi mdi-cellphone-basic"></i></button>
                                                                            <form class="" action="/api/follow_ups/follow_read" method="POST" id="follow_up_lead">
                                                                                <input type="hidden" name="lead" value="{{obj.data.lead.id}}" >
                                                                            <input type="submit" class="mdi mdi-file-restore" value="view all">
                                                                            </form>
                                                                        </td>
                                                                    </tr>
                                                                    {% endfor %}
                                                                    {% endfor %}
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>