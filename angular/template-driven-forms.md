# Template Driven Forms

- You need to import `FormsModule` for Angular to automatically "control" forms.
- You can access the `ngForm` object by assigning it to a template variable. This form object has several useful properties like "submitted", "hasError" etc.
- Adding `ngModel` to a form field let's angular know that a field is part of a form. The field value will then show up in the "value" property of that form object.
- The property name in the value object comes from the "name" attribute of the form field 
- Use the banana in a box syntax for 2-way data binding. For example, `<input name="name" [(ngModel)]="userSettings.name" />`.
- Use `ngNativeValidate` to have the browser validate forms.
- Angular automatically adds appropriate classes to a field as it is touched/modified.
- The classes angular adds to a field also have corresponding properties in the `ngModel` object.
- You can assign custom class names to a field (or any element for that matter) using the syntax `<input [class.field-error]="nameField.invalid" />`
