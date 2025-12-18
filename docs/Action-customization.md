## Customization Using Widget Flags

When the action GUI is created, widget flags are used to establish what is shown on the screen and how. Generally speaking, there are three ways to specify these widget flags:

### 1. Default Widget Flags

Default widget flags determine the default action GUI. For example, the default widget flags of the decimal [mv::gui::DecimalAction](https://github.com/ManiVaultStudio/core/blob/master/ManiVault/src/actions/DecimalAction.h) (derived from [mv::gui::NumericalAction](https://github.com/ManiVaultStudio/core/blob/master/ManiVault/src/actions/NumericalAction.h)) yield the following GUI:

![Decimal action with default widget flags](https://github.com/ManiVaultStudio/DeveloperWiki.wiki/raw/master/assets/decimal_action_default_widget_flags.png)  
*This is what the decimal action looks like with default widget flags `DecimalAction::WidgetFlag::Default`, which includes a spinbox and a slider.*

![Decimal action with spinbox widget flag only](https://github.com/ManiVaultStudio/DeveloperWiki.wiki/raw/master/assets/decimal_action_spinbox.png)  
*This is what the decimal action looks like with only the `DecimalAction::WidgetFlag::SpinBox` widget flag.*

![Decimal action with slider widget flag only](https://github.com/ManiVaultStudio/DeveloperWiki.wiki/raw/master/assets/decimal_action_slider.png)  
*This is what the decimal action looks like with only the `DecimalAction::WidgetFlag::Slider` widget flag.*

<details>
<summary><strong>Example: customizing the default look and feel of a decimal action</strong></summary>

```cpp
// Create the decimal actions
auto decimalActionDefault = new DecimalAction(this, "Decimal action (default flags)");
auto decimalActionSpinbox = new DecimalAction(this, "Decimal action (spinbox only)");
auto decimalActionSlider  = new DecimalAction(this, "Decimal action (slider only)");

// Set default widget flags
decimalActionSpinbox->setDefaultWidgetFlags(DecimalAction::WidgetFlag::SpinBox);
decimalActionSlider->setDefaultWidgetFlags(DecimalAction::WidgetFlag::Slider);

// Add the action widgets to the widget layout
layout->addWidget(decimalActionDefault->createWidget(this));
layout->addWidget(decimalActionSpinbox->createWidget(this));
layout->addWidget(decimalActionSlider->createWidget(this));
```
</details>

---

### 2. At Widget Creation Time

The look and feel of an action's GUI can also be modified when creating the action widget. This is achieved by supplying `WidgetAction::createWidget()` with widget flags directly.

```cpp
// Create a single decimal action
auto decimalAction = new DecimalAction(this, "Decimal action");

// Add decimal action widget with spinbox and slider
layout->addWidget(decimalAction->createWidget(this, DecimalAction::WidgetFlag::Default));

// Add decimal action widget with spinbox only
layout->addWidget(decimalAction->createWidget(this, DecimalAction::WidgetFlag::SpinBox));

// Add decimal action widget with slider only
layout->addWidget(decimalAction->createWidget(this, DecimalAction::WidgetFlag::Slider));
```

---

### 3. When Adding an Action to a Group-Based Action

When an action is added to a [mv::gui::GroupAction](https://github.com/ManiVaultStudio/core/blob/master/ManiVault/src/actions/GroupAction.h) derived action, custom widget flags can be specified, overriding default widget flags:

```cpp
// Create the group and decimal actions
auto decimalActions = new HorizontalGroupAction(this, "Decimal actions");
auto decimalActionA = new DecimalAction(this, "Decimal action A");
auto decimalActionB = new DecimalAction(this, "Decimal action B");

// Add decimal actions to the group
decimalActions->addAction(decimalActionA);
decimalActions->addAction(decimalActionB, DecimalAction::WidgetFlag::LineEdit); // Override widget flags

// Add the group action widget to the layout
layout->addWidget(decimalActions->createWidget(this));
```

---

## Customization Using Widget Post-Processing

In scenarios where the built-in look and behavior are insufficient, the created widget can be modified immediately after creation using the [mv::gui::WidgetAction::WidgetConfigurationFunction](https://github.com/ManiVaultStudio/core/blob/master/ManiVault/src/actions/WidgetAction.h#L41).

This can be set either via `setWidgetConfigurationFunction()` or passed inline to `createWidget()`:

```cpp
// Create the decimal action
auto decimalAction = new DecimalAction(this, "My decimal");

// Create a lambda to customize the widget
auto widgetEdit = [this](WidgetAction* action, QWidget* widget) -> void {
    auto spinBoxWidget = widget->findChild<QSpinBox*>("SpinBox");

    Q_ASSERT(spinBoxWidget);

    if (!spinBoxWidget)
        return;

    // Your widget customization goes here...
    spinBoxWidget->setStyleSheet("color: red;");
};

// Apply the widget configuration function
decimalAction->createWidget(this, widgetEdit);
```