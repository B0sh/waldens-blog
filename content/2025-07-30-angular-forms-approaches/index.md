+++
title = "What's the difference between FormsModule and ReactiveFormsModule in Angular?"
date = 2025-07-30
+++


I recently had an interview where I was quizzed on the difference between the Angular `FormsModule` and the `ReactiveFormsModule`, and honestly I didn't have a great answer. We only use `ReactiveFormsModule` in our codebase, so I wanted to investigate the difference and see if I'm missing out on something.

This post is a summary of my learnings from [the official documentation](https://angular.dev/guide/forms), which I recommend if you want to explore the topic in more detail.

### Why are there two types of forms?

It's a reasonable question to ask. The plainly named `FormsModule` gives you template-driven forms, so the form object is derived from the HTML Form written in your template. This minimizes the amount of JavaScript logic you need to manage the form state. 

`ReactiveFormsModule` on the other hand requires you to explicitly create the form structure ahead of time, but for that investment you get access to the raw form object. It's useful for robustness in your app like separation of concerns, scaling, and testing.



### Implementation Differences

Let's look at a basic implementation with one control that displays back to the user what value they typed in to demonstrate the two way binding.

```typescript
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-name-template',
  template: `
    Your Name: <input type="text" [(ngModel)]="name" />
    <br />
    User's Name: {{ name }}
  `,
  imports: [FormsModule],
})
export class NameTemplate {
  name = '';
}
```

For template-driven forms, the `name` variable is declared as a string, and then `[(ngModel)]` attaches the variable to the text input element. This automatically sets up the two way binding. You could add a button to reset the input with `this.name = '';` and Angular would know to update the form input as well.


```typescript
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-name-reactive',
  template: `
    Your Name: <input type="text" [formControl]="nameControl" />
    <br />
    User's Name: {{ nameControl.value }}
  `,
  imports: [ReactiveFormsModule],
})
export class NameReactive {
  nameControl = new FormControl('');
}
```

In the reactive version, we initialize a new `FormControl` instance and then pass it into the text input element using a directive, provided by the `ReactiveFormModule`.

In this simple case, these are actually equivalent. In the template driven example, Angular behind the scenes is transforming the variable `name` into a `FormControl` automatically for you. 

### A More Realistic Scenario

Forms get complicated. With one control it's hard to see the differences, so let's take a look at a more realistic scenario filling out an address block so we have more fields, and more features.

```typescript
export interface AddressForm {
  street: string;
  city: string;
  state: string;
  zipCode: string;
}
```

With template driven forms, all we have to do is define an object with that interface. The template just has to reference that object variable.

```typescript
@Component({
  selector: 'app-address-template',
  imports: [FormsModule],
  template: `
    <form (ngSubmit)="onSubmit()">
      Street: <input type="text" name="street" [(ngModel)]="address.street" /><br />
      City: <input type="text" name="city" [(ngModel)]="address.city" /><br />
      State: <input type="text" name="state" [(ngModel)]="address.state" /><br />
      Zip: <input type="text" name="zipCode" [(ngModel)]="address.zipCode" /><br />

      <button type="submit">Submit</button>
    </form>
  `,
})
export class AddressTemplate {
  address: AddressForm = {
    street: '',
    city: '',
    state: '',
    zipCode: '',
  };

  onSubmit() {
    console.log('Address:', this.address);
  }
}
```


With reactive forms, we have access to a `FormGroup` object that can hold multiple `FormControl` objects together. The `ReactiveFormsModule` gives us access to a directive to bind the form element and `FormGroup` together, and then we can reference the controls from there. It would look something like this:


```typescript
@Component({
  selector: 'app-address-reactive',
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="addressForm" (ngSubmit)="onSubmit()">
      Street: <input type="text" formControlName="street" /><br />
      City: <input type="text" formControlName="city" /><br />
      State: <input type="text" formControlName="state" /><br />
      Zip: <input type="text" formControlName="zipCode" /><br />

      <button type="submit">Submit</button>
    </form>
  `,
})
export class AddressReactive {
  addressForm = new FormGroup({
    street: new FormControl('', { nonNullable: true }),
    city: new FormControl('', { nonNullable: true }),
    state: new FormControl('', { nonNullable: true }),
    zipCode: new FormControl('', { nonNullable: true }),
  });

  onSubmit() {
      const address: AddressForm = this.addressForm.getRawValue();
      console.log('Address:', address);
  }
}
```

### Adding Validation

In order to show off the differences in the styles, let's try adding some form validation to both approaches. I want to make all the fields required, and add a string length to state and zipcode.

In reactive forms, you can add custom validator functions to each `FormControl` constructor. These `Validators.*` functions are built into Angular, but you can actually define your own validation functions to check for anything you want.

```typescript
  addressForm = new FormGroup({
    street: new FormControl('', { 
      nonNullable: true, 
      validators: [Validators.required] 
    }),
    city: new FormControl('', { 
      nonNullable: true, 
      validators: [Validators.required] 
    }),
    state: new FormControl('', { 
      nonNullable: true, 
      validators: [Validators.required, Validators.maxLength(2)] 
    }),
    zipCode: new FormControl('', { 
      nonNullable: true, 
      validators: [Validators.required, Validators.maxLength(5)] 
    }),
  });
```

On the submit button, you can then check for the `FormGroup.valid` property which is true when all controls pass their validators.

```html
<button type="submit" [disabled]="!addressForm.valid">Submit</button>
```


Template driven forms use HTML form properties to add validators, so we need to add `required` and `maxlength`.

```html
<form #addressForm="ngForm" (ngSubmit)="onSubmit()">
  Street: <input type="text" name="street" [(ngModel)]="address.street" required /><br />
  City: <input type="text" name="city" [(ngModel)]="address.city" required /><br />
  State: <input type="text" name="state" [(ngModel)]="address.state" required maxlength="2" /><br />
  Zip: <input type="text" name="zipCode" [(ngModel)]="address.zipCode" required maxlength="5" /><br />

  <button type="submit" [disabled]="!addressForm.valid">Submit</button>
</form>
```

With this approach it's doing double work as semantic properties for the browser and validation constraints for Angular. In our reactive forms example, we would need to go back and add the `maxlength` attribute in the template separately from the `FormGroup` definition to block the user from typing in additional characters. 

You'll also notice that we actually used the same method to check for validations in the template method as well.  With the template reference variable `#addressForm="ngForm"` you can get access to the underlying `NgForm` object, and therefore can use `[disabled]="!addressForm.valid"` to disable the submit button when the form is invalid in the same way. In this way you can always fallback and access the internal `FormGroup` or `FormControl` object in template based forms for things like validation where it can't be described from the template.

Custom validators are [possible](https://angular.dev/guide/forms/form-validation#adding-custom-validators-to-template-driven-forms) in template based forms as well using directives. 

### So, what should you choose?

The Angular documentation has this to say about choosing an approach:

> **Reactive forms:**
> Provide direct, explicit access to the underlying form's object model. Compared to template-driven forms, they are more robust: they're more scalable, reusable, and testable. If forms are a key part of your application, or you're already using reactive patterns for building your application, use reactive forms.
> 
> **Template-driven forms:**
> Rely on directives in the template to create and manipulate the underlying object model. They are useful for adding a simple form to an app, such as an email list signup form. They're straightforward to add to an app, but they don't scale as well as reactive forms. If you have very basic form requirements and logic that can be managed solely in the template, template-driven forms could be a good fit.


### My Opinions

I was surprised at how much of a complete solution template based forms were. I had an incorrect assumption that they were more limited than reactive forms, but it seems like pretty much everything has a solution in template based forms. Personally, I'm still going to be sticking with reactive forms. Yes, you can reach inside and pull out the `FormGroup` from the template based forms, but in my opinion if you're going to ever need to do that, you might as well just use reactive forms all the way. 

Like I said, we were already using reactive forms when I joined my company. Now it's clear to me why it was the obvious choice. We have large apps and often have forms with dozens of fields. One page actually swaps out the underlying reactive form object based on the document type, but otherwise reuses most of the page. Reactive forms makes this manageable and testable across many components.