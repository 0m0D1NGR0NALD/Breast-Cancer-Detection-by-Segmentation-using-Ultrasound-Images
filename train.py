import torch
import data

def accuracy(y_true,y_pred):
    correct = torch.eq(y_true,y_pred).sum().item()
    # How many of y_true == y_pred
    acc = (correct/len(y_pred))
    return acc

# Training and Testing Steps & Loop functions
def train_step(model,dataloader,loss_fn,accuracy,optimizer,device):
    model.train()
    train_loss, train_acc = 0,0
    for batch_num, (images,labels) in enumerate(dataloader):
        images,labels = images.to(device),labels.to(device)

        # Forward Pass
        logit = model(images)
        prob = torch.softmax(logit,dim=1)
        pred = torch.argmax(prob,dim=1)

        # Loss and Accuracy
        loss = loss_fn(logit,labels)
        train_loss += loss
        train_acc += accuracy(y_true=labels,y_pred=pred)

        # Zero grad, back prop, step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Average loss and accuracy across all batches
        train_loss /= len(dataloader)
        train_acc /= len(dataloader)

        return (train_loss,train_acc)

def val_step(model,dataloader,loss_fn,accuracy,device):
    model.eval()
    val_loss,val_acc = 0,0
    target_labels = []
    pred_probs = []

    # Turn off gradient tracking
    with torch.inference_mode():
        for batch_num, (images,labels) in enumerate(dataloader):
            images,labels = images.to(device),labels.to(device)

            # Forward Pass
            logit = model(images)
            prob = torch.softmax(logit,dim=1)
            pred = torch.argmax(prob,dim=1)

            pred_probs.append(prob.cpu())
            target_labels.append(labels.cpu())

            # Loss and Accuracy
            loss = loss_fn(logit,labels)
            val_loss += loss
            val_acc += accuracy(y_true=labels,y_pred=pred)
        
        pred_probs = torch.cat(pred_probs)
        target_labels = torch.cat(target_labels)

        # Average loss and accuracy across all batches
        val_loss /= len(dataloader)
        val_acc /= len(dataloader)

    return (val_loss,val_acc)



