templates.sobject_overview_structure = [
    '<ul class="nav nav-tabs" role="tablist">',
          '<li role="presentation"><a href="#overview" role="tab" data-toggle="tab">Overview</a></li>',
          '<li role="presentation"><a href="#fields" role="tab" data-toggle="tab">Fields</a></li>',
          '<li role="presentation"><a href="#childRelationships" role="tab" data-toggle="tab">Child Relationships</a></li>',
          '<li role="presentation"><a href="#validation" role="tab" data-toggle="tab">Validation</a></li>',
          '<li role="presentation"><a href="#download" role="tab" data-toggle="tab">Download</a></li>',
    '</ul>',

    '<div class="tab-content" id="sobject-content">',
      '<div role="tabpanel" class="tab-pane" id="overview">',
        '<table class="table">',
          '<tr>',
            '<td class="field-label">Label</td><td>{{ label }}</td>',
            '<td class="field-label">Key Prefix</td><td>{{ keyPrefix }}</td>',
          '</tr>',
          '<tr>',
            '<td class="field-label">Plural Label</td><td>{{ labelPlural }}</td>',
            '<td class="field-label">Name</td><td>{{ name }}</td>',
          '</tr>',
          '<tr>',
            '<td class="field-label">Createable</td><td>{{ createable }}</td>',
            '<td class="field-label">Custom</td><td>{{ custom }}</td>',
          '</tr>',
          '<tr>',
            '<td class="field-label">Deleteable</td><td>{{ deleteable }}</td>',
            '<td class="field-label">Feed Enabled</td><td>{{ feedEnabled }}</td>',
          '</tr>',
        '</table>',
      '</div>',    
      '<div role="tabpanel" class="tab-pane" id="fields">',
        '<table class="table">',
          '<tr>',
            '<th>Name</th>',
            '<th>Type</th>',
          '</tr>',
          '{{# each fields }}',
              '<tr>',
                '<td>{{ label }}</td>',
                '<td>{{ type }}</td>',
              '</tr>',
            '{{/each}}',
        '</table>',
      '</div>',
      '<div role="tabpanel" class="tab-pane" id="childRelationships">',
        '<table class="table">',
          '<thead>',
            '<tr>',
              '<th>Cascade Delete</th>',
              '<th>Child SObject</th>',
              '<th>Field</th>',
              '<th>Relationship Name</th>',
            '</tr>',
          '</thead>',
          '<tbody>',
            '{{# each child_relationships }}',
                '<tr>',
                  '<td>{{ cascadeDelete }}</td>',
                  '<td>{{ childSObject }}</td>',
                  '<td>{{ field }}</td>',
                  '<td>{{ relationshipName }}</td>',
                '</tr>',
            '{{/each}}',
          '</tbody>',
        '</table>',
      '</div>',
      '<div role="tabpanel" class="tab-pane" id="validation">',
        '<table class="table">',
          '<thead>',
            '<th>Id</th>',
            '<th>FullName</th>',
            '<th>ValidationName</th>',
            '<th>Description</th>',
            '<th>Error Display Field</th>',
            '<th>Error Message</th>',
            '<th>Formula</th>',
            '<th>Active</th>',
          '</thead>',
          '<tbody>',
            '{{# each validation_rules }}',
              '<tbody>',
                '<tr>',
                  '<td>{{ Id }}</td>',
                  '<td>{{ FullName }}</td>',
                  '<td>{{ ValidationName }}</td>',
                  '<td>{{ Metadata.description }}</td>',
                  '<td>{{ Metadata.errorDisplayField }}</td>',
                  '<td>{{ Metadata.errorMessage }}</td>',
                  '<td>{{ Metadata.errorConditionFormula }}</td>',
                  '<td>{{ Metadata.active }}</td>',
                '</tr>',
            '{{/each}}',
          '</tbody>',
        '</table>',
      '</div>',
    '</div>'
].join('\n');

templates.download_form_template = [
  '<div role="tabpanel" class="tab-pane" id="download">',
      '<form id="overview-form" method="post" action="/org/generatexcel">',
        '{{ csrf_token }}',
        '<div id="download-types">',
          '<input type="checkbox" id="overview" name="overview">Overview</input>',
          '<input type="checkbox" id="fields" name="fields">Field</input>',
        '</div>',
        '<textarea id="raw_sobject" name="raw_sobject" style="display: none;">{{ response }}</textarea>',
        '<button type="submit" id="excel-btn" class="btn btn-default">Excel</button>',
      '</form>',
  '</div>'
].join('\n');